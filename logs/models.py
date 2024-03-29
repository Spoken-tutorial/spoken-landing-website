from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TutorialProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.CharField(max_length=100)
    foss = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    time_completed = models.IntegerField(default=0)
    total_duration=models.IntegerField(null=True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    foss = models.CharField(max_length=100)
    language = models.CharField(max_length=50)
    total_tutorials = models.IntegerField(default=0)
    tutorials_completed = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    completion_status_sent = models.BooleanField(default=False)