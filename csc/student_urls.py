from django import views
from csc.student_views import *
from .views import *
from django.urls import path
from django.conf.urls import url
from .vle_views import *
from .ajax import get_foss_from_csc,raise_test_request,apply_for_test
app_name = 'csc'
urlpatterns = [
    path('', student_dashboard, name="student_dashboard"),
    path('courses/', student_courses, name="courses"),
    path('tests/', student_tests, name="student_tests"),
    path('student_change_test_status/', student_change_test_status, name="student_change_test_status"),
    path('list_foss_on_csc/', get_foss_from_csc, name="list_foss_on_csc"),
    path('raise_test_req/', raise_test_request, name="raise_test_req"),
    path('apply_for_test/', apply_for_test, name="apply_for_test"),
    
    
    path('download_certificate/', download_certificate, name="download_certificate"),
    path('request_retest/',request_retest, name="request_retest"),
    
    
   
    
]