from django.urls import path
from django.urls import re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


import os

from cms.api.views import StateList,DistrictList,DistrictDetail

urlpatterns = [
    path('states/',StateList.as_view(),name="state_list"),
    path('districts/<int:state_id>',DistrictDetail.as_view(),name="state_districts"),
    path('districts/',DistrictList.as_view(),name="district_list"),
]