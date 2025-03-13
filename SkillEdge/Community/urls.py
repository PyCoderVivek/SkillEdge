from django.urls import path
from . import views

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('comment/<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
    path('comment/<int:comment_id>/solution/', views.mark_solution, name='mark_solution'),
    path('user/<str:username>/posts/', views.user_posts, name='user_posts'),
    path('user/<str:username>/', views.community_profile, name='community_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/count/', views.notification_count, name='notification_count'),
] 