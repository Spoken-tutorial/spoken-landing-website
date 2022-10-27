from datetime import datetime
from email import message
from urllib import request


from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

import random, string
from csc.models import Student_certificate_course,CategoryCourses,Student_Foss
from django.db import IntegrityError
from csc.utils import is_user_vle, is_user_student
from django.template.loader import render_to_string
def send_pwd_mail(u):
    print(u.username)
    pwd = ''.join(random.choices(string.ascii_letters,k=10))
    print(pwd)
    u.set_password(pwd)
    u.save()
    
    from_email = getattr(settings, "NO_REPLY_MAIL", "no-reply@spoken-tutorial.org")
    print(from_email)
    subject = "Login credentials for Spoken Tutorial - CSC"
    if is_user_student(u):
        message = f"""
            Dear {u.get_full_name()},
            Thank you for registering under Spoken Tutorial(IIT Bombay) courses.
            Below are the login details for Spoken Tutorial Dashboard. 
            Link to Login: https://spoken-tutorial.in/login/

            username : {u.username}
            password : {pwd}

            Thanks & Regards,
            Team,
            Spoken Tutorial
            """
        path = 'student_mail_template.html'
    if is_user_vle(u):
        print('USER IS VLE')
        message = f"""
            Dear {u.get_full_name()},
            
            Welcome to IIT Bombay Spoken Tutorial Program. We are happy to be partnered with CSC Academy to
            empower youth from all over the country via VLEs.
            Please use the below Login details for the Spoken Tutorial Dashboard:
            Link to Login: https://spoken-tutorial.in/login/

            username : {u.username}
            password : {pwd}

            Please click the following training link to know the process of 
            Student Registration Instructions : https://docs.google.com/document/d/1z8-s4sSl7viPqJ8WAFeeNmoJUVLRPv2L9jLOrfN6ln0/edit?usp=sharing
            Course Allotment Instructions : https://docs.google.com/document/d/1Mv23iijOVuS6eCcHCgYKbbxopjk_SkSfExXW-61G2AQ/edit?usp=sharing
            
            In case of any query, please feel free to contact at animation-hackathon@cscacademy.org.
            
            Thanks & Regards,
            Team,
            Spoken Tutorial
            """
        path = 'vle_mail_template.html'
    html_content = render_to_string(path, {'full_name':u.get_full_name(),'username':u.username,'password':pwd})
    try:
        print(f"/n/nSending mail ; username,pwd : {u.username},{pwd}".ljust(40,'*'))
        send_mail(
    subject,
    message,
    from_email,
    [u.email],
    fail_silently=False,
    html_message = html_content
    )
        print("***************mail send******")
    except Exception as e:
        print(e)
        print(f"Failed to send mail to user : {u.email}")
    
def map_foss_to_student(student,fdate=datetime.today()):
    cert_courses = Student_certificate_course.objects.filter(student=student)
    print(f"\n\ncert_courses ***** {cert_courses}\n")
    l = []
    for course in cert_courses:
        fosses = CategoryCourses.objects.filter(certificate_category_id=course.cert_category_id).values('foss')
        for foss in fosses:
            try:
                Student_Foss.objects.create(student=student,cert_category=course.cert_category,csc_foss_id=foss['foss'],foss_start_date=fdate)
            except IntegrityError as e:
                print(e)