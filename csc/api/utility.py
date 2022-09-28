from email import message


from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

import random, string
from csc.models import Student_certificate_course,CategoryCourses,Student_Foss
from django.db import IntegrityError

def send_pwd_mail(u):
    
    pwd = ''.join(random.choices(string.ascii_letters,k=10))
    u.set_password(pwd)
    u.save()
    from_email = settings.CONTACT_MAIL
    subject = "Login credentials for Spoken Tutorial - CSC"
    message = f"""
        Dear Student,

        Please find below the login credentials for Spoken Tutorial - CSC Portal:
        username : {u.username}
        password : {pwd}

        Regards,
        Manager
        Spoken Tutorial | IIT Bombay
    """
    try:
        print(f"/n/nSending mail ; username,pwd : {u.username},{pwd}".ljust(40,'*'))
    #     send_mail(
    # subject,
    # message,
    # from_email,
    # ["ankitamk@gmail.com"],
    # # [u.email],
    # fail_silently=False,
    # )
    except Exception as e:
        print(e)
        print(f"Failed to send mail to user : {u.email}")
    
def map_foss_to_student(student):
    cert_courses = Student_certificate_course.objects.filter(student=student)
    print(f"\n\ncert_courses ***** {cert_courses}\n")
    l = []
    for course in cert_courses:
        fosses = CategoryCourses.objects.filter(certificate_category_id=course.cert_category_id).values('foss')
        for foss in fosses:
            try:
                Student_Foss.objects.create(student=student,csc_cert_course=course,csc_foss_id=foss['foss'])
            except IntegrityError as e:
                pass