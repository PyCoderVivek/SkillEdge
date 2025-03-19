from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Subject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)
    max_marks = models.IntegerField()
    obtained_marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.semester.name})"
