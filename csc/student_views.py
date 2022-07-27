
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import Student, StudentTest, Student_Foss, Test

def student_tests(request):
    context = {}
    student = Student.objects.get(user=request.user)
    context['student_id'] = student.id

    studentFoss = Student_Foss.objects.filter(student=student)
    vles = student.vle_id.all()
    tests_all = []
    test_status = {}
    for vle in vles:
        tests_vle = Test.objects.filter(vle=vle,foss__in=[x.csc_foss.spoken_foss for x in studentFoss])
        for test in tests_vle:
            tests_all.append(test)
            try:
                test_status[test] = StudentTest.objects.get(test=test).status
            except StudentTest.DoesNotExist:
                test_status[test] = 0
    studentTests = StudentTest.objects.filter(student=student)
    # tests_students = [x.test for x in tests_all]
    context['tests_all'] = tests_all
    context['test_status'] = test_status
    
    context['studentTests'] = studentTests
    return render(request,'csc/student_tests.html',context)

def student_change_test_status(request):
    data = {}
    status = request.GET.get('status')
    id = request.GET.get('id')  
    student = Student.objects.get(user=request.user)  
    try:
        st = StudentTest.objects.get(test_id=id)
        st.status = status
        st.save()
    except StudentTest.DoesNotExist:
        StudentTest.objects.create(test_id=id,student=student,status=status)  
    
    return HttpResponseRedirect(reverse('student:student_tests'))
    