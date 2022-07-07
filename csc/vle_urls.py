from django import views
from csc.vle_views import CSCLogin
from .views import *
from django.urls import path
from django.conf.urls import url
from .vle_views import *
app_name = 'csc'
urlpatterns = [
    path('login/', CSCLogin.as_view(), name="login"),
    path('vle/', vle_dashboard, name="vle_dashboard"),
    url(
      r'^get-foss-option/', 
      GetFossOptionView.as_view()
    ),
   
    
]