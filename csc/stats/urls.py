from django.urls import path
from django.urls import re_path


from csc.stats.views import *


urlpatterns = [
    path('',stats,name="stats_dashboard"),
    path('ajax_stats/',ajax_stats,name="ajax_stats"),
    path('ajax_csc_state_count/',get_csc_state_count,name="ajax_csc_state_count"),
    path('ajax_vle_detail/',ajax_vle_detail,name="ajax_vle_detail"),
    path('vle_stats/',VLEListView.as_view(),name="vle_stats"),
    path('student_stats/',StudentListView.as_view(),name="student_stats"),
    path('test_stats/', test_stats, name="test_stats"),
    path('download_test_stats/', download_test_stats, name="download_test_stats"),
    path('vle_report/',vle_report,name="vle_report"),
    path('student_report/',student_report,name="student_report"),
    path('test_report/',test_report,name="test_report"),
    path('ajax_get_cities/',ajax_get_cities,name="ajax_get_cities"),
]