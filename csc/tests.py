from django.test import TestCase
from .models import *

# Create your tests here.
def students_approve_tests(test_id,status,count,smax=50):
    test_id =test_id
    test = Test.objects.get(id=test_id)
    sf = Student_Foss.objects.filter(csc_foss__spoken_foss=test.foss)
    print(f"sf -- {sf}")
    temp=0
    for item in sf:
        print(f"For loop: {item}")
        if temp < count:
            try:
                student = item.student
                print(f"{temp} ---- {student}")
                print(f"{student.id} , {smax}")
                if student.id < smax:
                    print("student.id < smax")
                    st=StudentTest.objects.get(student=student,test=test)
                    st.status = status
                    st.save()
                    print('saved existinng studdent')
                    temp+=1
                else:
                    print(f"student.id > smax:")
            except StudentTest.DoesNotExist:
                print('exception')
                StudentTest.objects.create(student=student,test=test,status=status)
                print('new obbject created ')


