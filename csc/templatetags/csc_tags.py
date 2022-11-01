from django import template
import datetime
register = template.Library()
from csc.models import *

def is_today(value):
    print(f'today : {datetime.date.today()}')
    print(f'value : {value}')
    print(f'checking for date equaity : {value == datetime.date.today()}')

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
  mdlgradeentry = CSCTestAtttendance.objects.filter(test__foss_id=testfossid, student_id=studentid, status__gte=2, mdlgrade__gte=40.00)
  if mdlgradeentry:
    return True
  else:
    return False



@register.filter
def get_grade(studentid, testfossid):

  mdlgradeentry = CSCTestAtttendance.objects.filter(test__foss_id=testfossid, student_id=studentid, status__gte=2, mdlgrade__gte=40.00).order_by('-mdlgrade').first()

  return mdlgradeentry.mdlgrade