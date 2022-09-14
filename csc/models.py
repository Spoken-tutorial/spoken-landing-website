
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.forms import ChoiceField
from spokenlogin.models import *
from model_utils import Choices
from cms.models import State, District, City
from django.forms import widgets

REJECTED = 0
APPROVED = 1
PROGRAMME_TYPE_CHOICES = Choices(
    ('', ('-- None --')),('dca', ('DCA Programme')), ('individual', ('Individual Course'))
    )


class FossSuperCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'FOSS Category'
        verbose_name_plural = 'FOSS Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

class FossCategory(models.Model):
    foss = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    status = models.BooleanField(max_length=2)
    is_learners_allowed = models.BooleanField(max_length=2,default=0 )
    is_translation_allowed = models.BooleanField(max_length=2, default=0)
    # user = models.ForeignKey(User, on_delete=models.PROTECT )
    category = models.ManyToManyField(FossSuperCategory)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    show_on_homepage = models.PositiveSmallIntegerField(default=0, help_text ='0:Series, 1:Display on home page, 2:Archived')
    available_for_nasscom = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for nasscom' )
    available_for_jio = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for jio and spoken-tutorial.in' )
    csc_dca_programme = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for csc-dca programme' )
    class Meta(object):
        verbose_name = 'FOSS'
        verbose_name_plural = 'FOSSes'
        ordering = ('foss', )

    def __str__(self):
        return self.foss


class CertifiateCategories(models.Model):
    code = models.CharField(max_length=100, unique = True)
    title = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class CategoryCourses(models.Model):
    certificate_category = models.ForeignKey(CertifiateCategories,on_delete=models.CASCADE)
    foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.certificate_category.code} - {self.foss.foss}"




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

    def __str__(self):
        
        return f"{self.city},{self.district}"
    

class VLE(models.Model):
    csc = models.ForeignKey(CSC,on_delete=models.CASCADE) # edge case : 1 vle moves to another city, enrolls for csc with same email?? 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=100)
    status = models.BooleanField(default=True) # If the vle is inactivated for some reason

    class Meta:
        unique_together = ('csc','user')

    def __str__(self):
        return f"{self.user.first_name.title()} {self.user.last_name.title()}"

    
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
  
  programme_type = models.CharField(choices=PROGRAMME_TYPE_CHOICES,  max_length=100)
#   spoken_foss = models.IntegerField()
  spoken_foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
  created = models.DateField(blank=True,null=True)
  updated = models.DateField(auto_now = True, null=True)
  vle = models.ForeignKey(VLE,on_delete=models.CASCADE)
  
  #unique together
  class Meta(object):
    unique_together = (("spoken_foss","programme_type"),)
  def __str__(self):
      return self.spoken_foss.foss





# =========== Student models start ===================================

class Student(models.Model):
    student_id = models.CharField(max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # first_name = models.CharField(max_length=120)
    # last_name = models.CharField(max_length=120)
    gender = models.CharField(max_length=10,blank=True)
    dob = models.DateField(blank=True)
    # email = models.EmailField()
    phone = models.CharField(max_length=32,blank=True)
    edu_qualification = models.CharField(max_length=255,blank=True)
    vle_id = models.ManyToManyField(VLE) #if student joins another csc due to location change
    state = models.ForeignKey(State,on_delete=models.CASCADE,blank=True,null=True) 
    city = models.ForeignKey(City,on_delete=models.CASCADE,blank=True,null=True) 
    district = models.ForeignKey(District,on_delete=models.CASCADE,blank=True,null=True) 
    pincode = models.CharField(max_length=6,blank=True) 
    address = models.CharField(max_length=255,blank=True)
    date_of_registration = models.DateField()

    

class Student_certificate_course(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    cert_category = models.ForeignKey(CertifiateCategories,on_delete=models.CASCADE)
    programme_starting_date = models.DateField(blank=True,null=True)
    created = models.DateField(blank=True,null=True)
    updated = models.DateField(auto_now = True, null=True)

    class Meta:
        unique_together = ('student','cert_category')
    

class Student_Foss(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    csc_foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('student','csc_foss')


# =========== Student models ens ===================================



class Invigilator(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=32)
    vle = models.ManyToManyField(VLE)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='added_by_user')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"

class Test(models.Model):
    foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    tdate = models.DateField()
    ttime = models.TimeField()
    # invigilator = models.ManyToManyField(Invigilator,blank=True,null=True)
    publish = models.BooleanField()
    slug = models.SlugField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vle = models.ForeignKey(VLE,on_delete=models.CASCADE)
    note_student = models.TextField(blank=True,null=True)
    note_invigilator = models.TextField(blank=True,null=True)
    test_name = models.CharField(max_length=252,blank=True,null=True)
    #ToDO : Add status ; to mark if completed or cancellled

    # class Meta:
    #     widgets = {
    #         'tdate':widgets.DateInput(attrs={'type': 'date'})
    #     }
    def get_absolute_url(self):
        return f"{self.foss}"

    def __str__(self):
        if self.test_name:
            return self.test_name
        else:
            return f"{self.foss} - {self.tdate}"

class InvigilationRequest(models.Model):
    invigilator = models.ForeignKey(Invigilator,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    status = models.IntegerField() #0-pending, 1-accepted, 2-rejected
    
class StudentTest(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    status = models.IntegerField() #0 : Rejected, 1 : Approved
    test_status = models.IntegerField(default=0) #0: default - test not attended ; 1: attendance marked
    def __str__(self):
        return f"{self.id}"

    class Meta:
        unique_together = [['student', 'test']]

class TestRequest(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    foss = models.ForeignKey(FossCategory,on_delete=models.CASCADE)
    vle = models.ForeignKey(VLE,on_delete=models.CASCADE)
    status = models.IntegerField() 
    created = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.id}"