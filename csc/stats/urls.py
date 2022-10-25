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
    path('vle_report/',vle_report,name="vle_report"),
    path('student_report/',student_report,name="student_report")
    
    
    
    
]