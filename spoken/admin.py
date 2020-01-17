from django.contrib import admin

# Register your models here.
from .models import Products, Nav, Blended_workshops

admin.site.register(Products)
admin.site.register(Nav)
admin.site.register(Blended_workshops)
