from django import views
from csc.vle_views import CSCLogin
from .views import *
from django.urls import path
from .vle_views import vle_dashboard
app_name = 'csc'
urlpatterns = [
    path('login/', CSCLogin.as_view(), name="login"),
    path('vle/', vle_dashboard, name="vle_dashboard")

    
]