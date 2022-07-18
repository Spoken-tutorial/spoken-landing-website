from django import views
from csc.vle_views import CSCLogin
from .views import *
from django.urls import path

app_name = 'csc'
urlpatterns = [
    
    path('load_district/', load_district, name="load_district"),
    path('load_city/', load_city, name="load_city"),    
]