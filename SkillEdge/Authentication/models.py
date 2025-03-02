from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    interests = models.TextField(blank=True, null=True) 
    career_goals = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
