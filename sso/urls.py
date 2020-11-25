from django.urls import path

from .views import metadata_view

urlpatterns = [
    path('metadata/', metadata_view, name='sso_metadata'),
    
]
app_name = 'sso'