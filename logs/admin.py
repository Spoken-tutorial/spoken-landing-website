from django.contrib import admin

from .models import TutorialProgress, CourseProgress

admin.site.register(TutorialProgress)
admin.site.register(CourseProgress)