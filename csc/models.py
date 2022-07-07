
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.forms import ChoiceField
from spokenlogin.models import *
from model_utils import Choices

class CSC(models.Model):
    CSC_PLAN = [('College Level Subscription','College Level Subscription'),
                ('School Level Subscription','School Level Subscription')]
    
    csc_id = models.CharField(max_length=50) # id provided by csc
    institute = models.CharField(max_length=255)
    state = models.CharField(max_length=100) 
    city = models.CharField(max_length=100) 
    district = models.CharField(max_length=100) 
    block = models.CharField(max_length=100) 
    address = models.CharField(max_length=255) 
    pincode = models.CharField(max_length=6) 
    plan = models.CharField(choices=CSC_PLAN,max_length=100)
    activation_status = models.BooleanField(default=True) # If the csc is inactivated for some reason ; payment not done

    

class VLE(models.Model):
    csc = models.ForeignKey(CSC,on_delete=models.CASCADE) # edge case : 1 vle moves to another city, enrolls for csc with same email?? 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    status = models.BooleanField(default=True) # If the vle is inactivated for some reason

    class Meta:
        unique_together = ('csc','user')
    
class Transaction(models.Model):
    TRANSACTION_TENURE = [('quarterly','quarterly'),('biannually','biannually'),('annually','annually')]
    
    vle = models.ForeignKey(VLE,on_delete=models.CASCADE)
    csc = models.ForeignKey(CSC,on_delete=models.CASCADE)
    transcdate = models.DateField(null=False)
    tenure = models.CharField(choices=TRANSACTION_TENURE,max_length=10,null=True,blank=True)
    tenure_end_date = models.DateField(null=True,blank=True)

    class Meta:
        unique_together = ('vle','csc','transcdate')

class Vle_csc_foss(models.Model):
  PROGRAMME_TYPE_CHOICES = Choices(
    ('dca', ('DCA Programme')), ('individual', ('Individual Course'))
    )
  programme_type = models.CharField(choices=PROGRAMME_TYPE_CHOICES, default=PROGRAMME_TYPE_CHOICES.dca, max_length=100)
  spoken_foss = models.ForeignKey(SpokenFoss, on_delete=models.PROTECT)
  
  created = models.DateField(blank=True,null=True)
  updated = models.DateField(auto_now = True, null=True)
  # show = models.BooleanField(default=1)



    
    