from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Q
from .models import Post, Comment, Topic, Notification
from .forms import PostForm, CommentForm
from Authentication.models import Profile
from django.http import JsonResponse

def community_home(request):
    """Main community page with topic filters and post listing"""
    topics = Topic.objects.annotate(post_count=Count('posts'))
    
    # Filter by topic if provided
    topic_id = request.GET.get('topic')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'recent')
    
    posts = Post.objects.all().select_related('author', 'topic')
    
    # Apply filters
    if topic_id:
        posts = posts.filter(topic_id=topic_id)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query)
        )
    
    # Apply sorting
    if sort_by == 'recent':
        posts = posts.order_by('-created_at')
    elif sort_by == 'popular':
        posts = posts.annotate(upvote_count=Count('upvotes')).order_by('-upvote_count', '-created_at')
    elif sort_by == 'unanswered':
        posts = posts.annotate(comment_count=Count('comments')).filter(comment_count=0).order_by('-created_at')
    
    # Get recent activity
    recent_activity = Comment.objects.select_related('post', 'author').order_by('-created_at')[:5]
    
    context = {
        'topics': topics,
        'posts': posts,
        'current_topic_id': topic_id,
        'search_query': search_query,
        'sort_by': sort_by,
        'recent_activity': recent_activity,
    }
    return render(request, 'community/home.html', context)

@login_required
def create_post(request):
    """Create a new post"""
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created successfully!')
            return redirect('post_detail', post.id)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'topics': Topic.objects.all(),
    }
    return render(request, 'community/create_post.html', context)

def post_detail(request, post_id):
    """View a post and its comments"""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').order_by('created_at')
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Handle new comment
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Create notification for post author
            if request.user != post.author:
                Notification.objects.create(
                    user=post.author,
                    message=f"{request.user.username} commented on your post: {post.title}",
                    link=f"/community/post/{post.id}/"
                )
            
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', post.id)
    else:
        form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'community/post_detail.html', context)

@login_required
def upvote_post(request, post_id):
    """Upvote a post"""
    post = get_object_or_404(Post, id=post_id)
    
    # Toggle upvote
    if request.user in post.upvotes.all():
        post.upvotes.remove(request.user)
    else:
        post.upvotes.add(request.user)
        # Create notification if user is not the author
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                message=f"{request.user.username} upvoted your post: {post.title}",
                link=f"/community/post/{post.id}/"
            )
    
    return redirect('post_detail', post.id)

@login_required
def upvote_comment(request, comment_id):
    """Upvote a comment"""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Toggle upvote
    if request.user in comment.upvotes.all():
        comment.upvotes.remove(request.user)
    else:
        comment.upvotes.add(request.user)
        # Create notification if user is not the author
        if request.user != comment.author:
            Notification.objects.create(
                user=comment.author,
                message=f"{request.user.username} upvoted your comment on: {comment.post.title}",
                link=f"/community/post/{comment.post.id}/"
            )
    
    return redirect('post_detail', comment.post.id)

@login_required
def mark_solution(request, comment_id):
    """Mark a comment as the solution"""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Only post author can mark solution
    if request.user != post.author:
        messages.error(request, "Only the post author can mark a solution")
        return redirect('post_detail', post.id)
    
    # Update solution status
    post.comments.update(is_solution=False)
    comment.is_solution = True
    comment.save()
    
    # Update post solved status
    post.is_solved = True
    post.save()
    
    # Create notification
    if request.user != comment.author:
        Notification.objects.create(
            user=comment.author,
            message=f"Your comment was marked as the solution to: {post.title}",
            link=f"/community/post/{post.id}/"
        )
    
    messages.success(request, "Solution marked successfully!")
    return redirect('post_detail', post.id)

def user_posts(request, username):
    """View posts by a specific user"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    
    context = {
        'profile_user': user,
        'posts': posts,
    }
    return render(request, 'community/user_posts.html', context)

def community_profile(request, username):
    """View user's community profile"""
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')[:5]
    comments = Comment.objects.filter(author=user).order_by('-created_at')[:5]
    
    # Count total upvotes received
    post_upvotes = sum(post.upvotes.count() for post in Post.objects.filter(author=user))
    comment_upvotes = sum(comment.upvotes.count() for comment in Comment.objects.filter(author=user))
    total_upvotes = post_upvotes + comment_upvotes
    
    # Count accepted solutions
    accepted_solutions = Comment.objects.filter(author=user, is_solution=True).count()
    
    context = {
        'profile_user': user,
        'posts': posts,
        'comments': comments,
        'post_count': Post.objects.filter(author=user).count(),
        'comment_count': Comment.objects.filter(author=user).count(),
        'total_upvotes': total_upvotes,
        'accepted_solutions': accepted_solutions,
    }
    return render(request, 'community/profile.html', context)

@login_required
def notifications(request):
    """View user notifications"""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    
    # Mark all as read if requested
    if request.GET.get('mark_read'):
        notifications.update(is_read=True)
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'community/notifications.html', context)

@login_required
def notification_count(request):
    """Return the count of unread notifications for the current user"""
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'count': count})
