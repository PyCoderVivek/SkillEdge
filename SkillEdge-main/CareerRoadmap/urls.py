from django.urls import path
from . import views

urlpatterns = [
    path('', views.roadmap_dashboard, name='roadmap_dashboard'),
    path('create/', views.create_roadmap, name='create_roadmap'),
    path('view/<int:roadmap_id>/', views.view_roadmap, name='view_roadmap'),
    path('delete/<int:roadmap_id>/', views.delete_roadmap, name='delete_roadmap'),
    path('test-generation/', views.test_roadmap_generation, name='test_roadmap_generation'),
] 