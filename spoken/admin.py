from django.contrib import admin

# Register your models here.
from .models import Products, Nav, Blended_workshops,ContactMsg,Jobfair,Internship,Company 

admin.site.register(Products)
admin.site.register(Nav)
admin.site.register(Blended_workshops)
admin.site.register(ContactMsg)
admin.site.register(Jobfair)
admin.site.register(Internship)
