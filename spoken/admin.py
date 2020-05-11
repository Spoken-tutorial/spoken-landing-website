from django.contrib import admin
# Register your models here.
from .models import Products, Nav, Blended_workshops,ContactMsg,Jobfair,Internship,Company,Testimonials,MediaTestimonials,Award
from django import forms
from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.conf import settings
import csv
from django.db import IntegrityError
from django.db import transaction

# Register your models here.
admin.site.register(Nav)

@admin.register(ContactMsg)
class ContactMsgAdmin(admin.ModelAdmin):
	readonly_fields = ["name", "email", "subject","message"]
	list_display = ('name', 'email','subject')

class DifferentlySizedTextarea(forms.Textarea):
  def __init__(self, *args, **kwargs):
    attrs = kwargs.setdefault('attrs', {})
    attrs.setdefault('cols', 80)
    attrs.setdefault('rows', 5)
    super(DifferentlySizedTextarea, self).__init__(*args, **kwargs)

@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
	list_display = ('user_name', 'user_short_description','category','created')
	formfield_overrides = { models.TextField: {'widget': DifferentlySizedTextarea}}

@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
	list_display = ('title','year','order')

@admin.register(Blended_workshops)
class Blended_workshopsAdmin(admin.ModelAdmin):
	list_display = ('workshop_title','workshop_start_date','workshop_end_date','know_more_link')

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
	list_display = ('internship_title','internship_start_date','internship_end_date','know_more_link')

@admin.register(Company)
class CompanyAdmin(ImportExportModelAdmin):
    def save_related(self,request, form, formsets, change):
    	super(CompanyAdmin, self).save_related(request, form, formsets, change)
    	


@admin.register(Jobfair)
class JobfairAdmin(admin.ModelAdmin):
	list_display = ('jobfair_title','jobfair_start_date','jobfair_end_date','know_more_link')
	filter_horizontal = ('companies',)

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)

	def save_related(self,request, form, formsets, change):
		super(JobfairAdmin, self).save_related(request, form, formsets, change)
		j = form.instance
		if j.companies_csv.name:
			path = settings.MEDIA_ROOT+'/'+j.companies_csv.name
			with open(path, newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',')
				line_count = 0
				for row in spamreader:
					if line_count==0:
						line_count+=1
					else:
						for item in row:
							c = Company(name=item)
							try:
								with transaction.atomic():
									c.save()
							except IntegrityError:
								pass
							comp = Company.objects.filter(name=item)
							j.companies.add(*comp)


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ('product_name', 'product_url')

@admin.register(MediaTestimonials)
class ProductsAdmin(admin.ModelAdmin):
	list_display = ('user', 'user_short_desc','category','created')




