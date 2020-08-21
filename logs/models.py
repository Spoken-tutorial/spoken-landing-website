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