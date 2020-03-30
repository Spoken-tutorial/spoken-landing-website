from django.contrib import admin

# Register your models here.
from .models import Products, Nav, Blended_workshops,ContactMsg,Jobfair,Internship,Company,Testimonials,MediaTestimonials,Award

admin.site.register(Products)
admin.site.register(Nav)
admin.site.register(Blended_workshops)
admin.site.register(ContactMsg)
admin.site.register(Jobfair)
admin.site.register(Internship)
admin.site.register(Company)
admin.site.register(Testimonials)
admin.site.register(MediaTestimonials)
admin.site.register(Award)