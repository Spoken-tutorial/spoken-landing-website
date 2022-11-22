
from datetime import date
from multiprocessing import context
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import CSCTestAtttendance, CertifiateCategories, Student, StudentTest, Student_Foss, Test, VLE, TestRequest, Vle_csc_foss,CategoryCourses,FossCategory,Student_certificate_course
from .utils import upcoming_foss_tests,check_student_test_status
from .student_forms import RaiseTestRequestForm
from django.contrib.auth.decorators import login_required
from .decorators import is_student
from django.db.models import Q
from .utils import TEST_COMPLETED_BY_STUDENT
from django.conf import settings
from csc.utils import PASS_GRADE

TEST_WAITING_PERIOD = 10
def student_tests(request):
    context = {}
    student = Student.objects.get(user=request.user)
    context['student_id'] = student.id

    studentFoss = Student_Foss.objects.filter(student=student)
    vles = student.vle_id.all()
    tests_all = []
    test_status = {}
    for vle in vles:
        tests_vle = Test.objects.filter(vle=vle,foss__in=[x.csc_foss.foss for x in studentFoss])
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

@login_required
@is_student
def student_dashboard(request):
    context = {}
    student = Student.objects.get(user=request.user)
    sf = Student_Foss.objects.filter(student=student)
    courses = [x.cert_category for x in sf]

    indi = CertifiateCategories.objects.get(code='INDI')
    indi_fosses = [x.csc_foss for x in Student_Foss.objects.filter(student=student,cert_category__code='INDI').order_by('csc_foss__foss')]
    
    d = {}
    for course in courses:
        d[course] = [x.foss for x in CategoryCourses.objects.filter(certificate_category=course)]
    try:
        d.pop(indi)
    except:
        pass

    context['student'] = student
    context['CSC_ONLINE_TEST_URL'] = settings.CSC_ONLINE_TEST_URL
    context['courses'] = d
    context['fosses'] = indi_fosses
    context['vle'] = student.vle_id.all()[0]
    context['pass_grade'] = PASS_GRADE
    
    return render(request,'csc/student_dashboard.html',context)

@login_required
@is_student
def student_courses(request):
    context = {}
    student = Student.objects.get(user = request.user)
    student_foss = Student_Foss.objects.filter(student=student)
    in_progress_foss_data = {}
    vles = []
    context = {}
    # vles = VLE.objects.filter(user=request.user)
    
    individual_foss = {}
    fosses = [x['foss'] for x in FossCategory.objects.filter(available_for_jio=True).values('foss')]
    context['fosses'] = fosses
    courses = CertifiateCategories.objects.exclude(code__in=['INDI'])
    if request.GET.get('course_search'):
        search_term = request.GET.get('search_term')
        q_code = Q(certificate_category__code__icontains=search_term)
        q_title = Q(certificate_category__title__icontains=search_term)
        q_foss  = Q(foss__foss__icontains=search_term)
        courses = [x.certificate_category for x in CategoryCourses.objects.filter(q_code|q_title|q_foss)]
        
    else:
        courses = CertifiateCategories.objects.exclude(code__in=['INDI'])
    d = {}
    for course in courses:
        fosses = [x['foss__foss'] for x in CategoryCourses.objects.filter(certificate_category_id=course.id).values('foss__foss')]
        # if course.code in d:
        d[course] = fosses
    print(f"\n\n{d}\n\n")
    context['courses'] = d
     
    return render(request,'csc/student_courses.html',context)   

def student_tests(request):
    context = {}
    student = Student.objects.get(user=request.user)
    open_tests = CSCTestAtttendance.objects.filter(student=student,status=OPEN_TEST)
    completed_tests = CSCTestAtttendance.objects.filter(student=student,status__in=[TEST_COMPLETED_BY_STUDENT])
    context['open_tests']=open_tests
    context['completed_tests']=completed_tests
    # print(f"student.vle_id - {student.vle_id.all()}")
    # vles = VLE.objects.filter(id__in=[x.id for x in student.vle_id.all()])
    # csc = [(x.csc.id,x.csc.csc_id, x.csc.city) for x in vles]
    # # if len(csc) == 1:
    # vle = VLE.objects.get(csc_id = csc[0])
    # # vle_csc_foss = Vle_csc_foss.objects.filter(vle=vle)
    # # sf = Student_Foss.objects.filter(student=student,csc_foss__in = vle_csc_foss) 
    # sf = Student_Foss.objects.filter(student=student) 

    # # fosses = [(x.csc_foss.spoken_foss.foss,x.csc_foss.spoken_foss.id) for x in sf]
    # fosses = [x.csc_foss for x in sf]
    # applied = [x.foss for x in TestRequest.objects.filter(student=student)]
    # print(f'fosses : {fosses}')
    # print(f'applied : {applied}')
    # available_foss = [] 
    # for foss in fosses:
    #     if not foss in applied:
    #         available_foss.append((foss.foss,foss.id))
    # context['fosses'] = available_foss

    # context['csc'] = csc
    # testReqs = TestRequest.objects.filter(student=student)
    # context['test_requests'] = testReqs

    # student_foss = Student_Foss.objects.filter(student=student)
    # in_progress_foss_data = {}
    # for item in student_foss:
    #     csc_foss = item.csc_foss
    #     foss = csc_foss.foss
    #     vle = csc_foss.vle
        
    #     upcoming_tests = upcoming_foss_tests(foss,vle)
    #     applied = check_student_test_status(upcoming_tests,student)
    #     print(f'before : {upcoming_tests}')
    #     try:
    #         upcoming_tests.remove(applied)
    #     except Exception as e:
    #         print(e)

    #     print(f'after : {upcoming_tests}')
    #     in_progress_foss_data[foss] = {'applied' : applied, 'upcoming_tests' : upcoming_tests}

    # context['in_progress_foss_data'] = in_progress_foss_data
    return render(request,'csc/student_tests.html',context)

def download_certificate(request):
    data = {}
    print(f"download_certificate ************************************ ")
    return JsonResponse(data)
