from django import views
from csc.vle_views import CSCLogin
from .views import *
from django.urls import path
from django.conf.urls import url
from .vle_views import *
app_name = 'csc'
urlpatterns = [
    path('login/', CSCLogin.as_view(redirect_authenticated_user=True), name="login"),
    path('vle/', vle_dashboard, name="vle_dashboard"),
    path('students/', student_list, name="student_list"),
    path('student/<int:id>/', student_profile, name="student_profile"),
    path('courses/', courses, name="courses"),
    path('assign_foss/', assign_foss, name="assign_foss"),
    path('get_course_stats/', get_course_stats, name="get_course_stats"),

    url(
      r'^get-foss-option/', 
      GetFossOptionView.as_view()
    ),
   
    
]