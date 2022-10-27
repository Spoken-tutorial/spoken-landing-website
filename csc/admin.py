from django.contrib import admin
from .models import FossCategory,CertifiateCategories,CategoryCourses,CSCFossMdlCourses
# Register your models here.
admin.site.register(FossCategory)
admin.site.register(CertifiateCategories)
admin.site.register(CategoryCourses)
admin.site.register(CSCFossMdlCourses)

