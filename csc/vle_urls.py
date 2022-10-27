from django import views
from csc.vle_views import CSCLogin
from .views import *
from django.urls import path
from django.conf.urls import url
from .vle_views import *
from .ajax import ajax_mark_attendance
app_name = 'csc'
urlpatterns = [
    path('login/', CSCLogin.as_view(redirect_authenticated_user=True), name="login"),
    path('vle/', vle_dashboard, name="vle_dashboard"),
    path('students/', student_list, name="student_list"),
    path('student/<int:id>/', student_profile, name="student_profile"),
    path('courses/', courses, name="courses"),
    path('assign_foss/', assign_foss, name="assign_foss"),
    path('get_course_stats/', get_course_stats, name="get_course_stats"),
    path('get_stats/', get_stats, name="get_stats"),
    
    path('test/', test, name="test"),
    path('test_assign/', test_assign, name="test_assign"),
    path('test_list/', test_list, name="test_list"),
    path('add_test/', TestCreateView.as_view(), name="add_test"),
    path('mark_attendance/<int:id>', mark_attendance, name="mark_attendance"),
    # path('detail_test/<int:pk>', TestDetailView.as_view(), name="detail_test"),
    path('detail_test/<slug:slug>', TestDetailView.as_view(), name="detail_test"),
    # path('update_test/<int:pk>', TestUpdateView.as_view(), name="update_test"),
    path('update_test/<int:pk>', update_test, name="update_test"),
    path('delete_test/<int:pk>', TestDeleteView.as_view(), name="delete_test"),
    path('list_test/', TestListView.as_view(), name="list_test"),
    path('invigilator/', invigilator, name="invigilator"),
    path('invigilators/', invigilators, name="invigilators"),
    path('invigilator_dashboard/', invigilator_dashboard, name="invigilator_dashboard"),
    path('verify_invigilator_email/', verify_invigilator_email, name="verify_invigilator_email"),
    path('add_invigilator/', add_invigilator, name="add_invigilator"),
    path('review_invigilation_request/', review_invigilation_request, name="review_invigilation_request"),
    path('add_invigilator_to_test/', add_invigilator_to_test, name="add_invigilator_to_test"),
    # path('delete_invigilator/', delete_invigilator, name="delete_invigilator"),
    
    path('create_invigilator/', create_invigilator, name="create_invigilator"),
    path('view_invigilators/', view_invigilators, name="view_invigilators"),
    path('invigilators/<int:id>/', update_invigilator, name="update_invigilator"),
    path('invigilators/delete/<int:id>/', InvigilatorDeleteView.as_view(), name="delete_invigilator"),
    
    
    url(
      r'^get-foss-option/', 
      GetFossOptionView.as_view()
    ),
   
  #  ajax
    path('ajax_mark_attendance/', ajax_mark_attendance, name="ajax_mark_attendance"),
    path('check_vle_email/', check_vle_email, name="check_vle_email")

    
    
]