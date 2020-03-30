from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Products(models.Model):
	product_name = models.CharField(max_length=200)
	product_url = models.CharField(max_length=300)
	product_description = models.CharField(max_length=1000)
	logo = models.FileField(upload_to='logos/')
	updated = models.DateField(auto_now=True)

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

	def __str__(self):
		return self.nav_name


class Blended_workshops(models.Model):
	workshop_title = models.CharField(max_length=255)
	workshop_date = models.DateField()
	workshop_content = models.TextField()
	workshop_logo = models.FileField(upload_to='logos/workshop_logos/',blank=True,null=True)
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)

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
	internship_date = models.DateField()
	internship_desc = models.TextField()
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)

	def __str__(self):
		return self.internship_title

class Company(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Jobfair(models.Model):
	jobfair_title = models.CharField(max_length=255)
	jobfair_start_date = models.DateField(blank=True,null=True)
	jobfair_end_date = models.DateField(blank=True,null=True)
	jobfair_desc = models.TextField()
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)
	companies = models.ManyToManyField(Company)
	def __str__(self):
		return self.jobfair_title


class Testimonials(models.Model):
  user = models.ForeignKey(User, related_name = 'testimonial_created_by', on_delete=models.PROTECT )
  approved_by = models.ForeignKey(User, related_name = 'testimonial_approved_by', null=True, on_delete=models.PROTECT )
  user_name = models.CharField(max_length=200)
  actual_content = models.TextField()
  minified_content = models.TextField()
  short_description = models.TextField(blank=True,null=True)
  source_title = models.CharField(max_length=200, blank=True,null=True)
  source_link = models.URLField(blank=True,null=True)
  status = models.PositiveSmallIntegerField(default = 0)
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now = True, null=True)
  show = models.BooleanField(default=1)


class MediaTestimonials(models.Model):
    '''
    This model is required for storing audio / video testimonials
    * path contains the location of the file,
    * user is the person who has send the testimonial.
    '''
    # foss = models.ForeignKey(FossCategory, on_delete=models.PROTECT )
    foss = models.CharField(max_length=200,default="series")
    path = models.CharField(max_length=255)
    user = models.CharField(max_length=255)
    workshop_details = models.CharField(max_length=255, default='Workshop')
    content = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='testimonials/',blank=False,null=False,default='')

    class Meta(object):
        verbose_name = 'Media Testimonials'
        verbose_name_plural = 'Media Testimonials'

    def __str__(self):
        return self.path
