from django.db import models
from django.contrib.auth.models import User

class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Roadmap: {self.title}"

class RoadmapMilestone(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    time_frame = models.CharField(max_length=100, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Resource(models.Model):
    milestone = models.ForeignKey(RoadmapMilestone, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    resource_type = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.title
