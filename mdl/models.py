from django.db import models

# Create your models here.
class MdlUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=96)
    idnumber = models.CharField(max_length=765)
    firstname = models.CharField(max_length=300)
    lastname = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    class Meta(object):
        db_table = 'mdl_user'
        managed = False

class MdlQuizGrades(models.Model):
    id = models.BigIntegerField(primary_key=True)
    quiz = models.BigIntegerField()
    userid = models.BigIntegerField()
    grade = models.DecimalField(max_digits=12, decimal_places=5)
    timemodified = models.BigIntegerField()
    class Meta(object):
        db_table = 'mdl_quiz_grades'
        managed = False

class MdlQuizAttempts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    quiz = models.BigIntegerField()
    userid = models.BigIntegerField()
    attempt = models.IntegerField(unique=True)
    uniqueid = models.BigIntegerField(unique=True)
    layout = models.TextField()
    currentpage = models.BigIntegerField()
    preview = models.IntegerField()
    state = models.CharField(max_length=48)
    timestart = models.BigIntegerField()
    timefinish = models.BigIntegerField()
    timemodified = models.BigIntegerField()
    timemodifiedoffline = models.BigIntegerField()
    timecheckstate = models.BigIntegerField(null=True, blank=True)
    sumgrades = models.DecimalField(null=True, max_digits=12, decimal_places=5, blank=True)
    class Meta(object):
        db_table = 'mdl_quiz_attempts'
        managed = False



        