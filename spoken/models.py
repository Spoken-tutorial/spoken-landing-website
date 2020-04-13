from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices

# Create your models here.
class Products(models.Model):
	product_name = models.CharField(max_length=200)
	product_url = models.CharField(max_length=300)
	product_description = models.TextField()
	logo = models.FileField(upload_to='logos/')
	updated = models.DateField(auto_now=True)

	class Meta:
		verbose_name='Product'
		verbose_name_plural='Products'

	def __str__(self):
		return self.product_name


class Nav(models.Model):
	nav_name = models.CharField(max_length=255)
	nav_id = models.CharField(max_length=50)
	data_section = models.CharField(max_length=50)
	fa_icon = models.CharField(max_length=50, blank=True)
	back_image = models.FileField(upload_to='page_backgrounds/',blank=True,null=True)
	status = models.BooleanField(default=0)
	updated = models.DateField(auto_now=True)

	class Meta:
		verbose_name='Navigation Tab'
		verbose_name_plural='Navigation Tabs'

	def __str__(self):
		return self.nav_name


class Blended_workshops(models.Model):
	workshop_title = models.CharField(max_length=255)
	workshop_start_date = models.DateField(blank=True,null=True)
	workshop_end_date = models.DateField(blank=True,null=True)
	workshop_content = models.TextField()
	workshop_logo = models.FileField(upload_to='logos/workshop_logos/',blank=True,null=True)
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)

	class Meta:
		verbose_name='Blended Workshop'
		verbose_name_plural='Blended Workshop'

	def __str__(self):
		return self.workshop_title

class ContactMsg(models.Model):
	name = models.CharField(max_length=200)
	email = models.EmailField(max_length=200)
	subject = models.CharField(max_length=200)
	message = models.TextField()
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = "Mails"

	def __str__(self):
		return self.name+'-('+self.email+')'

class Internship(models.Model):
	internship_title = models.CharField(max_length=255)
	internship_start_date = models.DateField(blank=True,null=True)
	internship_end_date = models.DateField(blank=True,null=True)
	internship_desc = models.TextField()
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)

	def __str__(self):
		return self.internship_title

class Company(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name
	class Meta:
		verbose_name='Company'
		verbose_name_plural='Companies'

class Jobfair(models.Model):
	jobfair_id = models.CharField(max_length=50, blank=True,null=True)
	jobfair_title = models.CharField(max_length=255)
	jobfair_start_date = models.DateField(blank=True,null=True)
	jobfair_end_date = models.DateField(blank=True,null=True)
	jobfair_desc = models.TextField()
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)
	companies = models.ManyToManyField(Company)
	num_students_registered = models.IntegerField(default=0)
	num_students_placed = models.IntegerField(default=0)
	eligibility_criteria = models.TextField(default='')
	selection_process = models.TextField(default='')
	num_student_appeared = models.IntegerField(default=0)
	registration_start_date = models.DateField(blank=True,null=True)
	registration_end_date = models.DateField(blank=True,null=True)
	# location


	def __str__(self):
		return self.jobfair_title

class Testimonials(models.Model):
  user_name = models.CharField(max_length=200)
  user_short_description = models.CharField(max_length=300,blank=True,null=True,help_text="short description about user. Eg. college name, position")
  actual_content = models.TextField()
  CATEGORY = Choices(('spoken_tutorials', ('spoken tutorials')), ('school_system', ('school system')),('forums', ('forums')),('online_test', ('online test')),('health_nutrition', ('health & nutrition')))
  category = models.CharField(choices=CATEGORY, default=CATEGORY.spoken_tutorials, max_length=100)
  created = models.DateField(blank=True,null=True)
  updated = models.DateField(auto_now = True, null=True)
  show = models.BooleanField(default=1)

  def __str__(self):
  	return '%s - %s' % (self.user_name, self.user_short_description)

  class Meta(object):
        verbose_name = 'Text Testimonial'
        verbose_name_plural = 'Text Testimonials'
  

class MediaTestimonials(models.Model):
    '''
    This model is required for storing audio / video testimonials
    * path contains the location of the file,
    * user is the person who has send the testimonial.
    '''
    CATEGORY = Choices(('spoken_tutorials', ('spoken tutorials')), ('school_system', ('school system')),('forums', ('forums')),('online_test', ('online test')),('health_nutrition', ('health & nutrition')))
    category = models.CharField(choices=CATEGORY, default=CATEGORY.spoken_tutorials, max_length=100)
    user = models.CharField(max_length=255)
    user_short_desc = models.CharField(max_length=255,help_text='short description of user',default='')
    additional_details = models.CharField(max_length=255, default='Workshop',help_text='workshop, jobfair or other detail')
    content = models.TextField()
    created = models.DateField(auto_now_add=True)
    media = models.FileField(upload_to='testimonials/',blank=False,null=False,default='')
    show = models.BooleanField(default=1)

    class Meta(object):
        verbose_name = 'Media Testimonial'
        verbose_name_plural = 'Media Testimonials'

    def __str__(self):
        return '%s' % (self.user)

class Award(models.Model):
	title = models.CharField(max_length=500)
	year = models.IntegerField(default=2020)
	order = models.IntegerField(help_text="Award with lower order will appear first in the list")
	link = models.CharField(max_length=300)

	def __str__(self):
		return self.title


