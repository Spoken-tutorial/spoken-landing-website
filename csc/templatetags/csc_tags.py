from django import template
import datetime
register = template.Library()
from csc.models import *
from csc.utils import TEST_COMPLETED_BY_STUDENT,PASS_GRADE, TEST_ATTENDANCE_MARKED
from csc.utils import get_valid_animation_fosses

def is_today(value):
    return value == datetime.date.today()

register.filter('is_today', is_today)

def is_gte_today(value):
    return value <= datetime.date.today()

register.filter('is_gte_today', is_gte_today)


@register.filter
def get_csc_mdlcourseid(eventfossid):
  try:
    csccourse = CSCFossMdlCourses.objects.filter(foss=eventfossid)
  except CSCFossMdlCourses.DoesNotExist:
    return None

  return csccourse


@register.filter
def check_attendance(studentid, testfossid):
  try:
    print(testfossid)
    attendance = CSCTestAtttendance.objects.filter(test__foss_id=testfossid, student_id=studentid).first()
    print(attendance,"######################")
    return attendance
  except Exception as e:
    print(e)
    return None

  

# @register.filter
# def check_passgrade_exists(studentid, testfossid):
#   # valid_fosses = get_valid_animation_fosses()
#   valid_fosses = [x.test.foss.id for x in CSCTestAtttendance.objects.filter(student_id=studentid)]
#   if testfossid in valid_fosses:
#     try:
#       pass_entry = CSCTestAtttendance.objects.filter(test__foss__id=testfossid, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT, mdlgrade__gte=PASS_GRADE)
#       return pass_entry   
#     except:
#       return None  
#   else:
    # return None


@register.filter
def check_passgrade_exists(studentid, testfossid):
  try:
    grade_entry = CSCTestAtttendance.objects.filter(test__foss__id=testfossid, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT).first()
    
    if grade_entry.mdlgrade >= PASS_GRADE:
      result = "Pass"
    elif grade_entry.mdlgrade < PASS_GRADE:
      result =  "Fail"


    print(f"pass_entry for foss - {testfossid} - {grade_entry}")
    return grade_entry, result
  except:
    return None  



 
@register.filter(name='format_url')
def format_url(value):
    return value.foss.replace(' ', '+')