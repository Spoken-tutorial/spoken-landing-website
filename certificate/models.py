from django.db import models
from django.contrib.auth.models import User
from csc.models import CSCTestAtttendance

# Create your models here.

c_types = (
        ('ind', 'Individual Foss Course'),
)

class Certificate(models.Model):
    _type = models.CharField(max_length=50, choices=c_types)
    background = models.FileField(upload_to='backgrounds')
    parameters = models.TextField()
    text_template = models.FileField(upload_to='templates')

class Log(models.Model):
    key = models.CharField(max_length=25, unique=True)
    full_key = models.CharField(max_length=40, unique=True, null=True)
    test_attendance = models.ForeignKey(CSCTestAtttendance, on_delete=models.CASCADE)
