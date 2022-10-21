from genericpath import exists
from tokenize import group
import datetime
from .models import *
from .models import REJECTED, APPROVED 
from datetime import date,timedelta
from django.db.models import Count
from django.conf import settings

# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.platypus import Paragraph
# from reportlab.lib.units import cm

# from PyPDF2 import PdfFileWriter, PdfFileReader

# from io import StringIO, BytesIO

from django.http import HttpResponse

def is_user_vle(user):
    return user.groups.filter(name="VLE").exists()   

def is_user_student(user):
    return user.groups.filter(name="STUDENT").exists()   

def is_csc_team_role(user):
    return user.groups.filter(name="CSC-TEAM").exists()   

def is_user_invigilator(user):
    print("\n\n user is INVIGILATOR \n\n")
    return user.groups.filter(name="INVIGILATOR").exists()   

def get_upcoming_test_stats():
    print("1 ------- ")
    tests = Test.objects.filter(tdate__gte=datetime.datetime.now().date())
    d = {}
    for test in tests:
        approved = StudentTest.objects.filter(test=test,status=APPROVED).count()
        rejected = StudentTest.objects.filter(test=test,status=REJECTED).count()
        # key = test.test_name if test.test_name else test.foss.foss
        key = test.foss.foss
        d[key] = {'approved' : approved, 'rejected' : rejected,'date': test.tdate, 'time': test.ttime, 'id':test.id }
    return d

def get_courses_offered_stats():
    print("2 ------- ")
    d = {}

    dca = Student_certificate_course.objects.filter(cert_category__code='DCA').count()
    
    individual = Student_certificate_course.objects.filter(cert_category__code='INDI').count()
    
    d['dca'] = dca
    d['individual'] = individual
    print(d)
    return d

def get_programme_stats():
    print("3 ------- ")
    
    course_count_result = (Student_certificate_course.objects.values('cert_category__code').annotate(scount=Count('cert_category__code')).order_by())
    print(course_count_result)
    d = {}
    for item in course_count_result:
        d[item['cert_category__code']]=item['scount']
    course_count = [x for x in course_count_result]
    print(f"course_count\n\n\n\n{course_count}")
    return d
    return course_count


def get_foss_enroll_percent(vle):
    csc_foss = [x for x in FossCategory.objects.filter(available_for_jio=True)]
    d = {}

    total = Student_Foss.objects.filter(csc_foss__in = csc_foss).count()
    for item in csc_foss:        
        d[item.foss] = ((Student_Foss.objects.filter(csc_foss = item).count())/total)*100
    
    print(d)
    print("------------------------------------------------------------------------------------------------------------------------")
    return d


def upcoming_foss_tests(foss,vle):
    tests = Test.objects.filter(foss=foss,vle=vle,tdate__gt=date.today())
    return list(tests)

def check_student_test_status(test,student):
    studentTest = StudentTest.objects.filter(test__in=test,student=student)
    if studentTest:
        return studentTest[0].test
    return False

def getFirstName(name):
    formatted = name.split()
    if formatted:
        return formatted[0]
    return ''

def getLastName(name):
    formatted = name.split(maxsplit=1)
    if len(formatted)>1:
        return formatted[1]
    return ''

def get_tenure_end_date(tdate):
    print(f"Inside tenure date")
    subscription_period = getattr(settings, "CSC_SUBSCRIPTION_PERIOD", 100)
    print(f"subscription_period - {subscription_period} ")
    end_date = tdate + timedelta(100)
    print(f"*****1")
    print(f"end_date ****** {str(end_date)}")
    return end_date

