from django.contrib import admin
from .models import Topic, Post, Comment, Notification

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'post_count')
    search_fields = ('name', 'description')
    
    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'topic', 'created_at', 'is_solved', 'upvote_count', 'comment_count', 'views')
    list_filter = ('is_solved', 'topic', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    
    def upvote_count(self, obj):
        return obj.upvotes.count()
    upvote_count.short_description = 'Upvotes'
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author', 'created_at', 'is_solution', 'upvote_count')
    list_filter = ('is_solution', 'created_at')
    search_fields = ('content', 'author__username', 'post__title')
    
    def upvote_count(self, obj):
        return obj.upvotes.count()
    upvote_count.short_description = 'Upvotes'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
