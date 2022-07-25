from django import views
from csc.student_views import *
from .views import *
from django.urls import path
from django.conf.urls import url
from .vle_views import *
app_name = 'csc'
urlpatterns = [
    path('student_tests/', student_tests, name="student_tests"),
    path('student_change_test_status/', student_change_test_status, name="student_change_test_status"),
    
    
   
    
]