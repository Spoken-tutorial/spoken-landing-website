from django.db import models

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
	fa_icon = models.CharField(max_length=50)
	back_image = models.FileField(upload_to='page_backgrounds/')
	status = models.BooleanField(default=0)
	updated = models.DateField(auto_now=True)

	def __str__(self):
		return self.nav_name


class Blended_workshops(models.Model):
	workshop_title = models.CharField(max_length=255)
	workshop_date = models.DateField()
	workshop_content = models.TextField()
	workshop_logo = models.FileField(upload_to='logos/workshop_logos/')
	know_more_link = models.CharField(max_length=300)
	updated = models.DateField(auto_now=True)

	def __str__(self):
		return self.workshop_title


