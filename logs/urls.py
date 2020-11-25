from django.urls import path

from . import views
urlpatterns = [
    path('save_tutorial_progress/', views.save_tutorial_progress, name='save_tutorial_progress'),
    path('get_set_progress/', views.get_set_tutorial_progress, name='save_tutorial_progress'),  
]

app_name = 'logs'