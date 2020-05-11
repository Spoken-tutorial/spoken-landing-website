from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobfairs/', views.jobfairs, name='jobfairs'),
    path('jobfairs/<slug:jobfair_id>', views.jobfair_detail, name='jobfair_detail'),
    
]