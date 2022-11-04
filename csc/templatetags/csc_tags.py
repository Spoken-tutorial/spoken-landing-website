from django import template
import datetime
register = template.Library()
from csc.models import *
from csc.utils import TEST_COMPLETED_BY_STUDENT,PASS_GRADE
from csc.utils import get_valid_animation_fosses

def is_today(value):
    return value == datetime.date.today()

register.filter('is_today', is_today)


@register.filter
def get_csc_mdlcourseid(eventfossid):
  try:
    csccourse = CSCFossMdlCourses.objects.filter(foss=eventfossid)
  except CSCFossMdlCourses.DoesNotExist:
    return None

  return csccourse


@register.filter
def check_passgrade_exists(studentid, testfossid):
  # valid_fosses = get_valid_animation_fosses()
  valid_fosses = [x.test.foss.id for x in CSCTestAtttendance.objects.filter(student_id=studentid)]
  if testfossid in valid_fosses:
    print(f"TRUE FOR *************** {testfossid}")
    return CSCTestAtttendance.objects.filter(test__foss__id=testfossid, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT, mdlgrade__gte=PASS_GRADE)
  else:
    return True

  # # mdlgradeentry = CSCTestAtttendance.objects.filter(test__foss_id=testfossid, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT, mdlgrade__gte=PASS_GRADE)
  # mdlgradeentry = CSCTestAtttendance.objects.filter(test__foss__in=valid_fosses, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT, mdlgrade__gte=PASS_GRADE)
  # print(f"mdlgradeentry **** {testfossid} ******************** {mdlgradeentry}")
  # if mdlgradeentry:
  #   return True
  # else:
  #   return False



# @register.filter
# def get_grade(studentid, testfossid):

#   mdlgradeentry = CSCTestAtttendance.objects.filter(test__foss_id=testfossid, student_id=studentid, status__gte=TEST_COMPLETED_BY_STUDENT, mdlgrade__gte=PASS_GRADE).order_by('-mdlgrade').first()

#   return mdlgradeentry.mdlgrade