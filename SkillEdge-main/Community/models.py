from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Topic(models.Model):
    """Categories for posts"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, default="chat-dots")  # For Bootstrap icons
    
    def __str__(self):
        return self.name

class Post(models.Model):
    """Main model for questions/discussions"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, related_name='posts')
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    is_solved = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])
    
    def upvote_count(self):
        return self.upvotes.count()
    
    def comment_count(self):
        return self.comments.count()
    
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    """Responses to posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)
    is_solution = models.BooleanField(default=False)  # Marked by post author as solution
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    def upvote_count(self):
        return self.upvotes.count()
    
    class Meta:
        ordering = ['created_at']

class Notification(models.Model):
    """User notifications for community activity"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"
    
    class Meta:
        ordering = ['-created_at']
