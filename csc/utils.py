from django.db.models import OuterRef,Exists, Count, F, Value, Q
from genericpath import exists
from tokenize import group
import datetime

from mdl.models import MdlUser
from csc.models import *
# from csc.models import Test
# from .models import REJECTED, APPROVED 
from datetime import date,timedelta
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.platypus import Paragraph
# from reportlab.lib.units import cm

# from PyPDF2 import PdfFileWriter, PdfFileReader

# from io import StringIO, BytesIO

import random, string

TEST_OPEN=0
TEST_ATTENDANCE_MARKED=1
TEST_ONGOING=2
TEST_COMPLETED_BY_STUDENT=3
RETEST=4
PASS_GRADE=40.00

# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.platypus import Paragraph
# from reportlab.lib.units import cm

# from PyPDF2 import PdfFileWriter, PdfFileReader

# from io import StringIO, BytesIO

from django.http import HttpResponse

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
    return user.groups.filter(name="INVIGILATOR").exists()   

def get_upcoming_test_stats(vle):
    tests = Test.objects.filter(tdate__gte=datetime.datetime.now().date(),vle=vle)
    d = {}
    for test in tests:
        total_students = CSCTestAtttendance.objects.filter(test=test).count()
        key = test.foss.foss
        d[key] = {'total_students' : total_students,'date': test.tdate, 'time': test.ttime, 'id':test.id }
    return d

def get_courses_offered_stats():
    d = {}
    dca = Student_certificate_course.objects.filter(cert_category__code='DCA').count()
    individual = Student_certificate_course.objects.filter(cert_category__code='INDI').count()
    d['dca'] = dca
    d['individual'] = individual
    return d

def get_programme_stats():
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
    subscription_period = getattr(settings, "CSC_SUBSCRIPTION_PERIOD", 100)
    end_date = tdate + timedelta(100)
    return end_date

    
def get_valid_students_for_test(vle,test):
    foss = test.foss
    other_tests = Test.objects.filter(foss=foss).exclude(id=test.id)
    students = Student.objects.filter(vle_id=vle.id,student_foss__csc_foss_id=foss.id,student_foss__foss_start_date__lte=datetime.date.today()-timedelta(days=10)).annotate(assigned=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test=test))).annotate(ineligible=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test__in=other_tests))).annotate(test_taken=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test=test,status=TEST_COMPLETED_BY_STUDENT))).annotate(retest=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test=test,status=RETEST)))

    cscFossMdlCourses=CSCFossMdlCourses.objects.filter(Q(testfoss=foss)|Q(foss=foss))
    fosses = []
    for item in cscFossMdlCourses:
        fosses.append(item.testfoss)
        fosses.append(item.foss)
    other_tests = Test.objects.filter(foss__in=fosses).exclude(id=test.id)
    students = Student.objects.filter(vle_id=vle.id,student_foss__csc_foss_id__in=fosses,student_foss__foss_start_date__lte=datetime.date.today()-timedelta(days=10)).annotate(assigned=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test=test))).annotate(ineligible=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test__in=other_tests))).annotate(test_taken=Exists(CSCTestAtttendance.objects.filter(student_id=OuterRef('id'),test=test,status__gte=TEST_COMPLETED_BY_STUDENT))).distinct()
    
    return students

def get_all_foss_for_vle(vle):
    students = Student.objects.filter(vle_id=vle.id)
    fosses = Student_Foss.objects.filter(student_id__in=students).values('csc_foss').distinct()
    return FossCategory.objects.filter(id__in=[x['csc_foss'] for x in fosses]).order_by('foss')

def send_pwd_mail_to_invi(u):
    pwd = ''.join(random.choices(string.ascii_letters,k=10))
    u.set_password(pwd)
    u.save()
    invi = Invigilator.objects.get(user=u)
    from_email = getattr(settings, "NO_REPLY_MAIL", "no-reply@spoken-tutorial.org")
    subject = "Login credentials for Spoken Tutorial - CSC"
    message = f"""
            Dear {u.get_full_name()},
            Below are the login details for Spoken Tutorial Dashboard. 
            Link to Login: https://spoken-tutorial.in/login/

            username : {u.username}
            password : {pwd}

            Thanks & Regards,
            Team,
            Spoken Tutorial
            """
    try:
        send_mail(subject,message,from_email,[u.email],fail_silently=False)
        
        invi.password_mail_sent = 1
        invi.save()
    except Exception as e:
        invi.password_mail_sent = 0
        invi.save()
        print(e)
        print(f"Failed to send mail to user : {u.email}")

def send_mdl_mail(u,pwd):
    student = Student.objects.get(user=u)
    mdluser = MdlUser.objects.filter(email=u.email)[0]
    # pwd = ''.join(random.choices(string.ascii_letters,k=10))
    # u.set_password(pwd)
    # u.save()
    
    from_email = getattr(settings, "NO_REPLY_MAIL", "no-reply@spoken-tutorial.org")
    print(f"2 SENDING Email ************************ {u.email}")
    MDL_URL=getattr(settings, "MDL_URL", "")
    subject = "Login credentials for Moodle Spoken Tutorial - CSC"
    message = f"""
            Dear {u.get_full_name()},
            Below are the login details for Moodle Dashboard for Spoken Tutorial Test. 
            Link to Moodle Login: {MDL_URL}
            
            username : {mdluser.username}
            password : {pwd}

            Thanks & Regards,
            Team,
            Spoken Tutorial
            """
    print(f"3 SENDING Email ************************ {u.email}")
    try:
        print(f"4 SENDING Email ************************ {u.email}")
        send_mail(subject,message,from_email,[u.email],fail_silently=False)
        student.mdl_mail_sent = True
        student.save()
        print(f"5 SENDING Email ************************ {u.email}")
    except Exception as e:
        print(f"6 SENDING Email ************************ {u.email}")
        student.mdl_mail_sent = False
        student.save()
        print(e)
        print(f"Failed to send mail to user : {u.email}")
        print(f"7 SENDING Email ************************ {u.email}")
        
def get_valid_animation_fosses():
    course = CertifiateCategories.objects.get(code = 'IT07')
    fosses = [x.foss.id for x in CategoryCourses.objects.filter(certificate_category=course)]
    return FossCategory.objects.filter(id__in=fosses).order_by('foss')

def get_test_valid_fosses(vle):
    students = Student.objects.filter(vle_id=vle.id)
    fosses = [x['csc_foss'] for x in Student_Foss.objects.filter(student__in=students).values('csc_foss').distinct()]
    valid_fosses = CSCFossMdlCourses.objects.filter(Q(testfoss__in=fosses)|Q(foss__in=fosses)).order_by('testfoss')
    return valid_fosses

def get_invig(vle):
    invigilators = Invigilator.objects.filter(vle=vle).order_by('user__first_name')
    return invigilators
