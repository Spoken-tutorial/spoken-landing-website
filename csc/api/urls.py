from django.urls import path
from django.urls import re_path

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


import os

from csc.api.views import StudentListCreate,SutdentDetail,VLEListCreate,VLEDetail,studentTest
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Pastebin API')

schema_view = get_schema_view(
    openapi.Info(
        title="Spoken Tutorial - CSC API",
        default_version="v1",
        description="API for student data",
    ),
    url=f"http://127.0.0.1:8000/csc/",
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('students/',StudentListCreate.as_view(),name="create_list_student"),
    path('students/<str:user__email>',SutdentDetail.as_view(),name="detail_student"),
    path('vles/',VLEListCreate.as_view(),name="create_list_student"),
    path('vles/<str:user__email>',VLEDetail.as_view(),name="detail_student"),
    path('tests/students/<str:user__email>',studentTest,name="student_test"),
    # path('',schema_view)
]


urlpatterns += [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]