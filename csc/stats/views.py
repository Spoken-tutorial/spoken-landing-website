from django.shortcuts import render
from django.db.models import Count,F,Q
from django.http import JsonResponse
from django.views.generic import ListView
from django.views.decorators.csrf import  csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin
from csc.models import CSC,VLE,Student, FossCategory, CertifiateCategories, Student_Foss, Test
from cms.models import State, District
from csc.decorators import is_csc_team as dec_is_csc_team
from csc.utils import is_csc_team_role
from .utility import *

from datetime import datetime


@login_required
@dec_is_csc_team
def stats(request):
    context = {}
    
    total_vles = VLE.objects.count()-TEST_VLE_COUNT
    total_students = Student.objects.count()-TEST_STUDENT_COUNT
    total_foss = FossCategory.objects.filter(available_for_jio=True).count()
    total_certificate_course = CertifiateCategories.objects.count()
    context['total_vles'] = total_vles
    context['total_students'] = total_students
    context['total_foss'] = total_foss
    context['total_certificate_course'] = total_certificate_course
    context['total_test_conducted'] = Test.objects.filter(tdate__lt=datetime.now().date()).count()
    context['total_upcoming_tests'] = Test.objects.filter(tdate__gte=datetime.now().date()).count()
    
    student_gender = get_student_gender_stats()
    context['student_gender'] = student_gender
    sct = get_student_certi_stats()
    context['cert_count_tb'] = [x for x in sct]
    
    sft = get_student_foss_stats(0)
    context['foss_count_tb'] = [x for x in sft]
    csc_state = get_student_state_stats()
    context['csc_state'] = csc_state
    indi = CertifiateCategories.objects.get(code='INDI')
    student_indi_foss=Student_Foss.objects.filter(cert_category=indi).values('csc_foss__foss').annotate(count=Count('csc_foss')).order_by('-count')
    context['student_indi_foss'] = [x for x in student_indi_foss]
    
    return render(request, 'stats/stats.html', context)


def ajax_stats(request):
    data = {}
    
    student_gender = get_student_gender_stats()
    data['student_gender'] = [x for x in student_gender]
    student_category = get_student_category_stats()
    data['student_category'] = [x for x in student_category]
    student_occupation = get_student_occupation_stats()
    data['student_occupation'] = [x for x in student_occupation]
    student_course=get_student_certi_stats()
    data['student_course'] = [x for x in student_course]
    
    data['student_foss_1'] = [x for x in get_student_foss_stats(0,15)]
    data['student_foss_2'] = [x for x in get_student_foss_stats(15,30)]
    data['student_foss_3'] = [x for x in get_student_foss_stats(30,45)]
    data['student_foss_4'] = [x for x in get_student_foss_stats(45,60)]
    data['student_foss_5'] = [x for x in get_student_foss_stats(start=45)]
    
    csc_state = get_student_state_stats()
    data['csc_state'] = [x for x in csc_state]

    data['student_indi_foss_1'] = [x for x in get_student_foss_stats(0,15,'indi')]
    data['student_indi_foss_2'] = [x for x in get_student_foss_stats(15,30,'indi')]
    data['student_indi_foss_3'] = [x for x in get_student_foss_stats(30,45,'indi')]
    data['student_indi_foss_4'] = [x for x in get_student_foss_stats(45,60,'indi')]
    data['student_indi_foss_5'] = [x for x in get_student_foss_stats(start=45,type='indi')]
    
    return JsonResponse(data)
    
def get_csc_state_count(request):
    data = {}
    csc_state = CSC.objects.values('state').annotate(count=Count('state'),code=F('state'))
    csc_state = [x for x in csc_state]
    data['csc_state'] = csc_state
    return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    paginate_by = 100
    model = Student 
    template_name = 'stats/student_stats.html'
    
    
    def get_queryset(self):
        raw = 'Select DATEDIFF(CURDATE(), `csc_student`.`dob`) from `csc_student` u where u.`id`=`csc_student`.id'

        qs = super().get_queryset()
        qs = qs_students
        # qs = qs.annotate(age2=find_age)
        # qs = qs.annotate(age2=ExpressionWrapper(RawSQL(raw, ())/365),output_field=IntegerField())
        if self.request.GET.get('name'):
            name = self.request.GET.get('name')
            qs = qs.filter(Q(user__first_name__icontains=name)|Q(user__last_name__icontains=name)|Q(user__email__icontains=name))
        if self.request.GET.get('vle_name'):
            name = self.request.GET.get('vle_name')
            vles = VLE.objects.filter(Q(user__first_name__icontains=name)|Q(user__last_name__icontains=name)|Q(user__email__icontains=name))
            qs = qs.filter(vle_id__in=vles)
        if self.request.GET.get('csc'):
            csc = self.request.GET.get('csc')
            csc = CSC.objects.get(csc_id=csc)
            vle = VLE.objects.filter(csc=csc)
            qs = qs.filter(vle_id__in=vle)
        if self.request.GET.get('edu'):
            edu = self.request.GET.get('edu')
            qs = qs.filter(edu_qualification__icontains=edu)
        if self.request.GET.get('state'):
            state = self.request.GET.get('state')
            state_obj = State.objects.get(name=state)
            qs = qs.filter(state_id=state_obj.id)
        if self.request.GET.get('district'):
            district = self.request.GET.get('district')
            district_obj = District.objects.get(name=district)
            qs = qs.filter(district_id=district_obj.id)
            
        if self.request.GET.get('occupation'):
            occupation = self.request.GET.get('occupation')
            qs = qs.filter(occupation=occupation)
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        edu = Student.objects.values('edu_qualification').distinct().order_by('edu_qualification')
        context['edu'] = edu
        context['states'] = State.objects.all().order_by('name')
        context['districts'] = District.objects.all().order_by('name')
        occupation = Student.objects.values('occupation').distinct().order_by('occupation')
        context['occupation'] = occupation
        query_str = self.request.GET
        context['query_str'] = query_str
        return context
    
    
   
@method_decorator(login_required, name='dispatch')
class VLEListView(ListView):
    paginate_by = 100
    model = VLE 
    template_name = 'stats/vle_stats.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['states'] = State.objects.all().order_by('name')
        context['districts'] = District.objects.all().order_by('name')
        query_str = self.request.GET
        context['query_str'] = query_str
        return context
    def get_queryset(self):
        qs = super().get_queryset() 
        qs = qs_vle.annotate(Count('test'))
        print(vars(qs[0]))
        if self.request.GET.get('name'):
            name = self.request.GET.get('name')
            qs = qs.filter(Q(user__first_name__icontains=name)|Q(user__last_name__icontains=name)|Q(user__email__icontains=name))
        if self.request.GET.get('csc_id'):
            csc_id = self.request.GET.get('csc_id')
            qs = qs.filter(csc__csc_id=csc_id)
        if self.request.GET.get('state'):
            state = self.request.GET.get('state')
            qs = qs.filter(csc__state=state)
        if self.request.GET.get('district'):
            district = self.request.GET.get('district')
            qs = qs.filter(csc__district=district)
        return qs

def student_stats(request):
    context = {}
    return render(request, 'stats/student_stats.html', context)


def vle_stats(request):
    context = {}
    return render(request, 'stats/vle_stats.html', context)    

@csrf_exempt
def ajax_vle_detail(request):
    data = {}
    vle_id = request.GET.get('vle_id')
    vle = VLE.objects.get(id=vle_id)
    data['name'] = vle.user.get_full_name()
    data['email'] = vle.user.email
    data['phone'] = vle.phone
    data['csc_id'] = vle.csc.csc_id
    data['state'] = vle.csc.state
    data['district'] = vle.csc.district
    data['address'] = vle.csc.address
    data['pin'] = vle.csc.pincode
    data['registered_on'] = vle.user.date_joined
    print(f"Student.objects.filter(vle_id=vle_id) ****** {Student.objects.filter(vle_id=vle_id)}")
    data['total_students'] = Student.objects.filter(vle_id=vle_id).count()
    data['fosses'] = [x for x in Student_Foss.objects.filter(student__vle_id=vle_id).values('csc_foss__foss').annotate(count=Count('csc_foss'))]
    data['courses'] = [x for x in Student_Foss.objects.filter(student__vle_id=vle_id).values('cert_category__code','cert_category__title').annotate(count=Count('cert_category'))]
    data['students'] = [x for x in Student.objects.filter(vle_id=vle_id).values('user__first_name', 'user__last_name','user__email')]
    cert_category = CertifiateCategories.objects.get(code='INDI')
    data['indi_fosses'] = [x for x in Student_Foss.objects.filter(student__vle_id=vle_id,cert_category=cert_category).values('csc_foss__foss').annotate(count=Count('csc_foss'))]
    data['conducted_test'] = Test.objects.filter(vle=vle, tdate__lt=datetime.now().date()).count()
    data['upcoming_test'] = Test.objects.filter(vle=vle, tdate__gte=datetime.now().date()).count()
    
    return JsonResponse(data)

@login_required
def student_report(request):
    context = {}
    context['total_students'] = Student.objects.count()
    student_course=Student_Foss.objects.values('cert_category__code','cert_category__title').annotate(count=Count('cert_category'))
    context['student_course'] = student_course
    student_foss=Student_Foss.objects.values('csc_foss__foss').annotate(count=Count('csc_foss')).order_by('csc_foss')
    context['student_foss'] = student_foss
    student_gender = Student.objects.values('gender').annotate(count=Count('gender'))
    context['student_gender'] = student_gender
    student_occupation = Student.objects.values('occupation').annotate(count=Count('occupation')).order_by('occupation')
    context['student_occupation'] = student_occupation
    edu = Student.objects.values('edu_qualification').distinct().annotate(count=Count('edu_qualification')).order_by('edu_qualification')
    context['edu'] = edu
    student_category = Student.objects.values('category').annotate(count=Count('category')).order_by('category')
    context['student_category'] = student_category
    student_state = Student.objects.values('state__name').annotate(count=Count('state')).order_by('state')
    context['student_state'] = student_state
    student_district = Student.objects.values('district__name').annotate(count=Count('district')).order_by('district')
    context['student_district'] = student_district
    
    return render(request, 'stats/student_report.html', context)

@login_required
@dec_is_csc_team   
def vle_report(request):
    context = {}
    csc_state = CSC.objects.values('state').annotate(count=Count('state')).order_by('state')
    context['csc_state'] = csc_state
    csc_district = CSC.objects.values('district').annotate(count=Count('district')).order_by('district')
    context['csc_district'] = csc_district
    
    return render(request, 'stats/vle_report.html', context)

@login_required
@dec_is_csc_team   
def test_report(request):
    context = {}
    all_foss = FossCategory.objects.annotate(upcoming_tests = Count('test', distinct=True, filter=Q(test__tdate__gte=datetime.now().date())), conducted_tests=Count('test', distinct=True, filter=Q(test__tdate__lt=datetime.now().date())), upcoming_students=Count('student_foss', distinct=True), appeared_students=Count('student_foss', distinct=True), all_certificates=Count('categorycourses', distinct=True))
    context['all_foss'] = all_foss
    return render(request, 'stats/test_report.html', context)