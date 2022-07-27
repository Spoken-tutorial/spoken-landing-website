from genericpath import exists
from tokenize import group
import datetime
from .models import Test, StudentTest, Student_Foss, Vle_csc_foss
from .models import REJECTED, APPROVED 

def is_user_vle(user):
    print("\n\n user is VLE \n\n")
    return user.groups.filter(name="VLE").exists()   

def is_user_student(user):
    print("\n\n user is Student \n\n")
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


