from genericpath import exists
from tokenize import group
import datetime
from .models import Test, StudentTest, Student_Foss, Vle_csc_foss
from .models import REJECTED, APPROVED 
from datetime import date

def is_user_vle(user):
    return user.groups.filter(name="VLE").exists()   

def is_user_student(user):
    return user.groups.filter(name="STUDENT").exists()   

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
        key = test.test_name if test.test_name else test.foss.foss
        d[key] = {'approved' : approved, 'rejected' : rejected,'date': test.tdate, 'time': test.ttime, 'id':test.id }
    return d

def get_courses_offered_stats():
    print("2 ------- ")
    d = {}
    dca = Student_Foss.objects.filter(csc_foss__programme_type='dca').count()
    individual = Student_Foss.objects.filter(csc_foss__programme_type='individual').count()
    d['dca'] = dca
    d['individual'] = individual
    print(d)
    return d

def get_programme_stats(type):
    print("3 ------- ")
    csc_fosses = Vle_csc_foss.objects.filter(programme_type=type)
    print(f"csc_fosses\n{csc_fosses}")
    # Student_Foss.objects.filter(csc_foss=csc_foss)
    d = {}
    for item in csc_fosses:
        print(item)
        d[item.spoken_foss.foss] = Student_Foss.objects.filter(csc_foss=item).count()
    print(d)
    return d


def get_foss_enroll_percent(vle):
    csc_foss = [x for x in Vle_csc_foss.objects.filter(vle=vle)]
    d = {}
    print("------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------")
    print(f"csc_foss *** {csc_foss}")
    total = Student_Foss.objects.filter(csc_foss__in = csc_foss).count()
    for item in csc_foss:
        print(item)
        print(item.spoken_foss.foss)
        print(Student_Foss.objects.filter(csc_foss = item))
        d[item.spoken_foss.foss] = ((Student_Foss.objects.filter(csc_foss = item).count())/total)*100
    
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

