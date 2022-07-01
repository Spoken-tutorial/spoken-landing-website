from django.urls import path

from . import views
from . import api
urlpatterns = [
    path('', views.home, name='home'),
    path('jobfairs/', views.jobfairs, name='jobfairs'),
    path('jobfairs/<slug:jobfair_id>', views.jobfair_detail, name='jobfair_detail'),
    path('tutorial-search/', views.TutorialSearch.as_view(), name= "tutorial_search"),
    path('api/tutorial-search/', api.TutorialSearchAPI.as_view(), name= "tutorial_search_api"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update_progress/', views.update_progress, name='update_progress'),
]