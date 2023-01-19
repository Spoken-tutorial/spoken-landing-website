from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.db.models import OuterRef,Exists,Q, Exists, Subquery
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse,reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View,ListView,DeleteView,DetailView,UpdateView
from django.views.generic.edit import CreateView
from django.http import FileResponse

from csc.models import *
from mdl.models import *
from spokenlogin.models import *
from certificate.models import Log

from .cron import add_vle,add_transaction
from .decorators import is_vle
from .models import TEST_OPEN
from .utils import *
from .vle_forms import *
from certificate.generator import generate

import logging
import random
import requests
import string
import hashlib
from django.http import FileResponse
from reportlab.pdfgen import canvas
import io

STUDENT_ENROLLED_FOR_TEST = 0
ATTENDANCE_MARKED = 1

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):         
    return ''.join(random.choice(chars) for _ in range(size))

class JSONResponseMixin(object):
  """
  A mixin that can be used to render a JSON response.
  """
  def render_to_json_response(self, context, **response_kwargs):
    """
    Returns a JSON response, transforming 'context' to make the payload.
    """
    return JsonResponse(
        self.get_data(context),
        **response_kwargs
    )

  def get_data(self, context):
    """
    Returns an object that will be serialized as JSON by json.dumps().
    """
    # Note: This is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return context

class CSCLogin(LoginView):
    template_name = 'csc/login.html'
    extra_context = {}

    def get_redirect_url(self):
        if is_user_vle(self.request.user): return reverse('csc:vle_dashboard')
        if is_user_student(self.request.user): return reverse('csc:vle_dashboard')
        # ToDo if student ; redirect to student dashboard

@login_required
@is_vle
def vle_dashboard(request):
    context = {}
    vle = VLE.objects.filter(user=request.user).first()

    context['vle'] = vle
    context['user'] = request.user
    context['upcoming_test_stats'] = get_upcoming_test_stats(vle)
    context['courses_offered_stats'] = get_courses_offered_stats()
    context['total_students_enrolled'] = Student.objects.filter(vle_id=vle).count()
    context['total_tests_completed'] = Test.objects.filter(vle=vle).count()
    context['total_upcoming_tests'] = Test.objects.filter(vle=vle,tdate__gte=datetime.datetime.today().date()).count()
    context['total_certificates_issued'] = StudentTest.objects.filter(status=4).count() #ToDo check condition
    student_ids = [x.id for x in Student.objects.filter(vle_id=vle.id)]
    context['enroll_training'] = Student_Foss.objects.filter(student_id__in=student_ids).count()
    context['enroll_test'] = CSCTestAtttendance.objects.filter(student_id__in=student_ids).count()
    context['certificates'] = CSCTestAtttendance.objects.filter(student_id__in=student_ids,mdlgrade__gte=PASS_GRADE).count()
    
    return render(request, 'csc/vle.html', context)
   
@login_required
@is_vle
def courses(request):
  context = {}
  vles = VLE.objects.filter(user=request.user)
  for vle in vles:
    individual_foss = {}
    fosses = FossCategory.objects.filter(available_for_jio=True)
    indi_students = Student_certificate_course.objects.filter(cert_category__code='INDI', student__in=Student.objects.filter(vle_id=vle.id)).values_list('student_id')
    
    for item in fosses:
      students = Student_Foss.objects.filter(csc_foss=item.id, student__in=indi_students).count()
      individual_foss[item.foss] = {'total_students':students}
 
    context['individual_foss'] = individual_foss
    vle = VLE.objects.filter(user=request.user)[0]
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
      d[course] = fosses
    context['courses'] = d
    
  return render(request,'csc/courses.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class GetFossOptionView(JSONResponseMixin, View):
  def dispatch(self, *args, **kwargs):
    return super(GetFossOptionView, self).dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
    programme_type = self.request.POST.get('programme_type')
    context = {}
    foss_option = "<option value=''>---------</option>"
    if programme_type == 'dca':
        fosses = FossCategory.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
    else:
        fosses = FossCategory.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')
    for foss in fosses:
      foss_option += "<option value=" + str(foss.id) + ">" + str(foss.foss) + "</option>"
    context = {
      'spoken_foss_option' : foss_option,
    }
    return self.render_to_json_response(context)

@login_required
@is_vle
def student_list(request):
  context={}
  vle = VLE.objects.filter(user=request.user).first()
  students = []
  course = request.GET.get('course')
  foss = request.GET.get('foss')
  name = request.GET.get('name')
  # dates = request.GET.get('dates')
  findividual = FossCategory.objects.filter(available_for_jio=True)
  context['foss_individual'] = [x for x in findividual]
  indi_id = CertifiateCategories.objects.get(code="INDI").id
  indi_course = Student_certificate_course.objects.filter(student_id=OuterRef('id'),cert_category_id=indi_id)
  s = Student.objects.filter(vle_id=vle.id).annotate(indi=Exists(indi_course))
  distinct_courses = set()
  vle_courses = Student_certificate_course.objects.filter(student__in=s) 
  # vle_courses = Student_certificate_course.objects.all()
  for item in vle_courses:
    # print(item.cert_category)
    distinct_courses.add(item.cert_category)
  context['distinct_courses'] = distinct_courses
  distinct_foss = set()
  vle_fosses = Student_Foss.objects.filter(student__in=s)
  for item in vle_fosses:
    distinct_foss.add(item.csc_foss)
  l = list(distinct_foss)
  l.sort(key=lambda x: x.foss.title())
  context['distinct_foss'] = l
  # all_students = Student.objects.filter(vle_id=vle.id)
  if name!=None:
    context['search_name'] = name
    s = s.filter(Q(user__first_name__icontains=name)|Q(user__last_name__icontains=name)|Q(user__email__icontains=name))
  if course!='0' and course!=None:
    try:
      context['search_course'] = CertifiateCategories.objects.get(id=course)
    except Exception as e:
      print(e)
    if CertifiateCategories.objects.get(id=course).code == 'INDI':
      context['is_indi'] = True
    try:
      s = s.filter(id__in=[x.student.id for x in Student_certificate_course.objects.filter(cert_category__id=course)])
    except Exception as e:
      print(e)
  if foss!='0' and foss!=None:
    try:
      context['search_foss'] = FossCategory.objects.get(id=foss)
    except Exception as e:
      print(e)
    try:
      s = s.filter(id__in=[x.student.id for x in Student_Foss.objects.filter(csc_foss=foss)])
    except Exception as e:
      print(e)
  if not (course or foss or name):
    context['is_indi'] = True
  for item in s:
    students.append(item)
  context['students'] = students
  context['students'] = s
  
  return render(request,'csc/students_list.html',context)


def student_profile(request,id):
  context={}
  student = Student.objects.get(id=id)
  initial={'fname': student.user.first_name , 'lname': student.user.last_name, 'state' :student.state}
  form = StudentForm(instance=student,initial=initial)
  context['form'] = form
  s_categories = Student_certificate_course.objects.filter(student=student)
  d = {}
  for category in s_categories:
    fosses = [x.csc_foss.foss for x in Student_Foss.objects.filter(student=student,cert_category=category.cert_category)]
    d[category.cert_category] = fosses
  context['courses'] = d
  return render(request,'csc/student_profile.html',context)

@csrf_exempt
def get_course_stats(request):
  vles = VLE.objects.filter(user=request.user)
  stats = {}
  fosses = []
  enrollment = []
  for vle in vles:
    csc_foss = Vle_csc_foss.objects.filter(vle=vle)
    for item in csc_foss:
      foss = item.spoken_foss.foss
      stats[foss] = Student_Foss.objects.filter(csc_foss=item).count()
      fosses.append(foss)
      enrollment.append(Student_Foss.objects.filter(csc_foss=item).count())

  return JsonResponse({'stats':stats,'fosses':fosses,'enrollment':enrollment,'len':len(fosses)})

class TestListView(ListView):
  model = Test
  template_name = 'csc/test_list.html'
  context_object_name = 'tests'
  paginate_by = 25

  def get_context_data(self, **kwargs):
    context = super(TestListView, self).get_context_data(**kwargs)
    vle = VLE.objects.filter(user = self.request.user).first()
    tests = Test.objects.filter(vle = vle)
    # tests = Test.objects.filter(vle = vle).annotate(attendance=ExpressionWrapper(F('tdate')==date.today(),output_field=BooleanField()))
    page = self.request.GET.get('page')
    paginator = Paginator(tests, self.paginate_by)
    try:
      tests = paginator.page(page)
    except PageNotAnInteger:
      tests = paginator.page(1)
    except EmptyPage:
      tests = paginator.page(paginator.num_pages)
    context['tests'] = tests
    
    test_req = [x for x in TestRequest.objects.filter(vle=vle)]
    context['test_req'] = test_req

    return context


@method_decorator(login_required, name='dispatch')
class TestCreateView(CreateView):
  model = Test
  template_name = 'csc/test_form.html'
  # fields = ['test_name','foss','tdate','ttime','note_student','note_invigilator','publish']
  fields = ['foss','tdate','ttime','publish']
  success_url = reverse_lazy('csc:list_test')

  def get_form(self, *args, **kwargs):
      form = super(TestCreateView, self).get_form(*args, **kwargs)
      vle = VLE.objects.filter(user=self.request.user).first()
      vle_foss = Vle_csc_foss.objects.filter(vle=vle)
      fosses = FossCategory.objects.filter(id__in=[x.spoken_foss.id for x in vle_foss])
      form.fields['foss'].queryset = fosses
      form.fields['tdate'].widget = widgets.DateInput(attrs={'type': 'date'})
      form.fields['ttime'].widget = widgets.DateInput(attrs={'type': 'time'})     
      return form

  def get_form_kwargs(self):
    kwargs = super(TestCreateView, self).get_form_kwargs()
    # kwargs['invi'] = self.request.user # pass the 'user' in kwargs
    return kwargs

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # user = self.request.user
    # context["ticket_list"] = user.ticket_set.all()
    vle = VLE.objects.filter(user=self.request.user).first()
    context['tests'] = Test.objects.filter(vle=vle)
    context['invigilators'] = Invigilator.objects.filter(vle=vle)
    return context
  
  def form_valid(self, form):
    vle = VLE.objects.filter(user=self.request.user).first()
    form.instance.vle = vle 

    messages.success(self.request,"Test added successfully.")
    return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TestDeleteView(DeleteView):
  model = Test
  template_name = 'csc/test_confirm_delete.html'
  success_url = reverse_lazy('csc:list_test')

  def form_valid(self, form):
    print('form is valid')

@method_decorator(login_required, name='dispatch')
class TestDetailView(DetailView):
  model = Test
  template_name = 'csc/test_detail.html'
  context_object_name = 'test'
  

@method_decorator(login_required, name='dispatch')
class TestUpdateView(UpdateView):
  model = Test
  template_name = 'csc/test_update_form.html'
  context_object_name = 'test'
  # fields = ('test_name','foss', 'tdate', 'ttime', 'note_student', 'note_invigilator', 'publish' )
  fields = ('foss', 'tdate', 'ttime',  'publish' )
  

  def get_success_url(self):
    messages.success(self.request,"Test updated successfully.")
    return reverse_lazy('csc:detail_test', kwargs={'pk': self.object.id})

  def get_form(self, *args, **kwargs):
      form = super(TestUpdateView, self).get_form(*args, **kwargs)
      vle = VLE.objects.filter(user=self.request.user).first()
      vle_foss = Vle_csc_foss.objects.filter(vle=vle)
      fosses = FossCategory.objects.filter(id__in=[x.spoken_foss.id for x in vle_foss])
      form.fields['foss'].queryset = fosses
      form.fields['tdate'].widget = widgets.DateInput(attrs={'type': 'date'})
      form.fields['ttime'].widget = widgets.DateInput(attrs={'type': 'time'})
      t = str(self.get_object().ttime).split(' ')[0]
      form.fields['ttime'].initial = t
      return form

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    vle = VLE.objects.filter(user=self.request.user).first()
    id = vle.id
    vle = VLE.objects.filter(user=self.request.user).first()
    invigilationRequestForm = InvigilationRequestForm(vle_id=id,test_id=self.get_object().id)
    context['invigilationRequestForm'] = invigilationRequestForm
    t = str(self.get_object().ttime).split(' ')[0]
    context['t']=t
    test = self.get_object()
    students = [x.student for x in StudentTest.objects.filter(test = test)]
    context['students'] = students
    return context

def invigilators(request):
  context = {}
  form = InvigilatorForm()
  if request.method == 'POST':
    form = InvigilatorForm(request.POST)
    if form.is_valid():
      email = form.cleaned_data['email']
      fname = form.cleaned_data['fname']
      lname = form.cleaned_data['lname']
      phone = form.cleaned_data['phone']
      try:
        user = User.objects.create(
                            username=email,first_name=fname,last_name=lname,
                            email=email,is_staff=0,is_active=1
                        )
        password = ''.join([ random.choice(string.ascii_letters+string.digits) for x in range(8)])
        enc_password = make_password(password)
        user.password = enc_password
        user.save()
        invigilator=Invigilator.objects.create(user=user,phone=phone,added_by=request.user)
        group = Group.objects.get(name='INVIGILATOR')
        group.user_set.add(user)
        messages.success(request,"Invigilator added successfully.")
      except Exception as e:  
        print(f"Exception while creating invigilator user: {e}")
        messages.error(request,"Error occurred while adding invigilator.")
      
      return render(request, 'invigilators.html', {'form': form})

  context['form'] = form
  vle = VLE.objects.filter(user=request.user).first()
  context['invigilators']  = Invigilator.objects.filter(vle=vle)
  return render(request, 'csc/invigilators.html',context)

@csrf_exempt
def verify_invigilator_email(request):
  USER_AND_INVIGIlATOR = 1
  USER_NOT_INVIGIlATOR = 2
  NOT_USER = 0
  MULTIPLE_USER = 3
  USER_AND_OWN_INVIGIlATOR = 4
  data = {}
  data['status'] = 0
  email = request.GET.get('email','')
  if email:
    try:
      user = User.objects.get(email=email)
      is_invigilator = Invigilator.objects.filter(user=user)
      invigilator_role = is_user_invigilator(user)
      if (is_invigilator or invigilator_role):
        vle = VLE.objects.filter(user=request.user)[0]
        invigilator = is_invigilator[0]
        if(vle in invigilator.vle.all()):
          data['status'] = USER_AND_OWN_INVIGIlATOR
          data['fname'] = user.first_name
          data['lname'] = user.last_name
          data['phone'] = is_invigilator[0].phone
        else:
          data['status'] = USER_AND_INVIGIlATOR
          data['fname'] = user.first_name
          data['lname'] = user.last_name
          data['phone'] = is_invigilator[0].phone

        return JsonResponse(data)
      else:
        data['status'] = USER_NOT_INVIGIlATOR
        data['fname'] = user.first_name
        data['lname'] = user.last_name
        # data['fname'] = user.first_name
    except User.MultipleObjectsReturned as e:
      print(f"User.MultipleObjectsReturne : {e}")
      data['status'] = MULTIPLE_USER
    except User.DoesNotExist:
      data['status'] = NOT_USER
  return JsonResponse(data)

# @csrf_exempt
def add_invigilator(request):
  vle = VLE.objects.filter(user=request.user).first()
  try:
    invigilator_email = request.POST.get('invigilator_email')
    invigilator_exist = request.POST.get('flag',False)
    
    invigilator_user = User.objects.get(email=invigilator_email)
    if invigilator_exist:
      invigilator = Invigilator.objects.get(user=invigilator_user)
    else:
      invigilator = Invigilator.objects.create(user=invigilator_user,phone=request.POST.get('phone'),added_by=request.user)
    
    invigilator.vle.add(vle)
    messages.success(request,"Invigilator successfullly assigned to CSC.")
  except Exception as e:
    print(f"Exception : {e}")
    messages.error(request,"An error occcured while adding invigilator.")
  
  data = {}
  return JsonResponse(data)


def invigilator_dashboard(request):
  context = {}
  invigilator = Invigilator.objects.get(user=request.user)
  pending = InvigilationRequest.objects.filter(invigilator=invigilator,status=0)
  accepted = InvigilationRequest.objects.filter(invigilator=invigilator,status=1)
  rejected = InvigilationRequest.objects.filter(invigilator=invigilator,status=2)
  all = InvigilationRequest.objects.filter(invigilator=invigilator)
  context['pending'] = pending
  context['accepted'] = accepted
  context['rejected'] = rejected
  context['all'] = all
  return render(request,'csc/invigilator_dashboard.html',context)

def add_invigilator_to_test(request):
  data = {}
  context = {}
  test = request.POST.get('test_id')  
  test_id = request.POST.get('test',test)  
  invigilators = request.POST.getlist('invigilators')
  test = Test.objects.get(id=int(test_id))
  for invigilator in invigilators:
    InvigilationRequest.objects.create(invigilator_id=int(invigilator),test=test,status=0)
  
  return HttpResponseRedirect(reverse('csc:update_test',kwargs={'pk':test_id}) )

def review_invigilation_request(request):
  status = request.GET.get("review")
  id = request.GET.get("item")
  obj = InvigilationRequest.objects.get(id=id)
  obj.status = int(status)
  obj.save()
  print(f'status : {request.GET.get("review")}')
  return HttpResponseRedirect(reverse('csc:invigilator_dashboard') )

def get_stats(request):
  data = {}
  data['upcoming_tests'] = get_upcoming_test_stats()
  data['course_type_offered'] = get_courses_offered_stats()
  data['course_count_result'] = get_programme_stats()
  return JsonResponse(data)

def mark_attendance(request,id):
  context = {}
 
  test = Test.objects.get(id=id)
  # st = [x.student for x in StudentTest.objects.filter(test=test)]
  st = [(x.student,x.status) for x in CSCTestAtttendance.objects.filter(test=test)]
  context['test'] = test
  context['students'] = st
  total_enrolled = len(st)
  attending = StudentTest.objects.filter(test_status=1).count()
  pending = total_enrolled - attending
  context['total_enrolled'] = total_enrolled
  context['attending'] = attending
  context['pending'] = pending
  
  if request.method == 'POST':
    student_attendance = request.POST.getlist('student_attendance')
    #present
    CSCTestAtttendance.objects.filter(test=test,student_id__in=student_attendance,status__in=[TEST_OPEN,TEST_ATTENDANCE_MARKED]).update(status=TEST_ATTENDANCE_MARKED)
    #absent
    b=CSCTestAtttendance.objects.filter(test=test,status=TEST_ATTENDANCE_MARKED).exclude(student_id__in=student_attendance).update(status=0)
    st = [(x.student,x.status) for x in CSCTestAtttendance.objects.filter(test=test)]
    context['students'] = st
  
  total_enrolled = CSCTestAtttendance.objects.filter(test=test).count()
  pending = CSCTestAtttendance.objects.filter(test=test,status=STUDENT_ENROLLED_FOR_TEST).count()
  attendance_marked = total_enrolled - pending
  context['total_enrolled'] = total_enrolled
  context['attending'] = attendance_marked
  context['pending'] = pending
  return render(request,'csc/mark_attendance.html',context)

@csrf_exempt
def check_vle_email(request):
  data = {}
  email = request.POST.get('email','')
  print(f"email - :{email}")
  # Code to be used later when csc adds date payload in api
  # last_update_date = VLE.objects.order_by('user__date_joined').last().user.date_joined
  # delta_date = last_update_date - timedelta(2)
  # payload = {'date':delta_date}
  url = getattr(settings, "URL_FETCH_VLE", "http://exam.cscacademy.org/shareiitbombayspokentutorial")
  # response = requests.get(url,params=payload)
  response = requests.get(url)
  data['status'] = 0
  if response.status_code == 200:
      result = response.json()['req_data']
      # result = response.json()
      # result = result['req_data']
      for item in result:
        if email == item['email']:
            logging.debug("Found email matching csc.")
            try:
                csc = CSC.objects.get(csc_id=item['csc_id'])
            except CSC.DoesNotExist:
                print(f"**csc - {item['csc_id']} does not exists")
                CSC.objects.create(
                    csc_id=item.get('csc_id'),institute=item.get('institute_name',''),state=item.get('state',''),
                    city=item.get('city',''),district=item.get('district',''),block=item.get('block',''),
                    address=item.get('address',''),pincode=item.get('pincode',''),plan=item.get('plan',''),
                    activation_status=1
                )
                csc = CSC.objects.get(csc_id=item.get('csc_id'))
            add_vle(item,csc)
            vle = VLE.objects.get(user__email=email)
            add_transaction(vle,csc,item['transcdate'])
            # messages.add_message(request,messages.INFO,'hello')
            data['status'] = 1
  else:
    data['status'] = 2
    
  return JsonResponse(data)



# Test related views start
def test(request):
  context = {}
  form = TestForm(user=request.user)
  if request.method == 'POST':
    form = TestForm(request.POST,user=request.user)
    if form.is_valid():
      test_data=form.save(commit=False) 
      vle = VLE.objects.filter(user=request.user)[0]
      test_data.vle = vle
      test_data.save()
      form.save_m2m() 
      messages.add_message(request,messages.SUCCESS,f'Test added successfully.')
  context['form'] = form
  
  return render(request,'csc/test.html',context)
  
def test_assign(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  students = [x['id'] for x in Student.objects.filter(vle_id=vle.id).values('id')]
  tests = Test.objects.filter(vle=vle,status=TEST_OPEN).order_by('-tdate','foss__foss')
  context['tests'] = tests
  test = request.POST.get('test')
  if test and test!='0':
    context['test'] = test
    try:
      test = tests.get(id=int(test))
      context['test'] = test.id
      foss = test.foss
      context['students'] = get_valid_students_for_test(vle,test)
    except Exception as e:
      print(e)
  else:
    return render(request,'csc/test_assign.html',context)
  
  if request.method == 'POST' and request.POST.get('action_type') == 'add_students':
    assigned_students = request.POST.getlist('students')
    try:
      # fossMdlCourse = CSCFossMdlCourses.objects.filter(foss=foss)[0] #ToDo Change
      fossMdlCourse = CSCFossMdlCourses.objects.filter(testfoss=foss)[0] 
      mdlcourse_id = fossMdlCourse.mdlcourse_id
      mdlquiz_id = fossMdlCourse.mdlquiz_id
      for email in assigned_students:
        user = User.objects.get(Q(username=email) | Q(email=email))
        student = Student.objects.get(user=user)
        try:
          mdluser=MdlUser.objects.get(email=email)
        except MdlUser.DoesNotExist:
          pwd = ''.join(random.choices(string.ascii_letters,k=10))
          encryp_pwd = hashlib.md5((pwd).encode('utf-8')).hexdigest()
          mdluser = MdlUser.objects.create(username=email,firstname=user.first_name,lastname=user.last_name,email=email,password=encryp_pwd,mnethostid=1,confirmed=1)
          send_mdl_mail(user,pwd)
          mdluser = MdlUser.objects.get(email=email)
        except MdlUser.MultipleObjectsReturned as e:
          mdluser=MdlUser.objects.filter(email=email)[0]
          print(e)
        try:
          ta = CSCTestAtttendance.objects.create(test=test,student=student,mdluser_id=mdluser.id,mdlcourse_id=mdlcourse_id,status=0,mdlquiz_id=mdlquiz_id)
        except IntegrityError as e:
          print(e)
          try:
            ta= CSCTestAtttendance.objects.get(test=test,student=student,mdluser_id=mdluser.id,mdlcourse_id=mdlcourse_id,status=4,mdlquiz_id=mdlquiz_id)
            ta.status=0
            ta.attempts=ta.attempts+1
            ta.save()
          except CSCTestAtttendance.DoesNotExist as e:
            pass
      if request.POST.get('action_type') == 'add_students':
        nta = CSCTestAtttendance.objects.filter(test=test,status=TEST_OPEN).exclude(student__user__email__in=assigned_students)
        for item in nta:
          item.delete()
      else:
        print(f"\n\n action type is NOT add_students **************************** ")
      messages.add_message(request,messages.SUCCESS,f'Test assigned to the students.')
      
    except Exception as e:
      print(e)
      messages.error(request,"No test in moodle for the selected foss.Please contact support.")
      return render(request,'csc/test_assign.html',context) 
  return render(request,'csc/test_assign.html',context)


def test_list(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  tests = Test.objects.filter(vle=vle).annotate(upcoming_students = Count('csctestatttendance', distinct=True, filter=Q(csctestatttendance__status__lte=2)), appeared_students = Count('csctestatttendance', distinct=True, filter=Q(csctestatttendance__status__gt=2)))
  context['tests'] = tests
  return render(request,'csc/test_list.html',context)

def test_students(request, pk):
  context = {}
  tests = CSCTestAtttendance.objects.filter(test=pk)
  context['tests'] = tests
  context['test'] = Test.objects.get(id=pk)
  return render(request,'csc/test_students.html', context)

def update_test(request,pk):
  context = {}
  if request.method == 'GET':
    test = Test.objects.filter(id=pk)[0]
    d = model_to_dict(test)
    td = model_to_dict(test)
    td['foss'] = test.foss.id
    form = TestForm(initial=td,user=request.user)  
    # form = TestForm(initial=model_to_dict(test),user=request.user)  
  if request.method == 'POST':
    t = Test.objects.get(id=pk)
    form = TestForm(request.POST,instance=t,user=request.user)
    if form.is_valid():
      form.save()
      messages.add_message(request,messages.SUCCESS,f'Test updated.')
  
  context['form'] = form
  
  return render(request,'csc/update_test.html',context)

def invigilator(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  invigilators = Invigilator.objects.filter(vle=vle)
  context['invigilators']=invigilators
  form_empty = InvigilatorForm()
  context['form_empty']=form_empty
  
  form = InvigilatorForm()
  add = request.POST.get('add')
  edit = request.POST.get('edit')
  
  if request.method == 'GET':
    if request.GET.get('invi'):
      invi = request.GET.get('invi')
      invi_obj = Invigilator.objects.get(id=invi)
      i = model_to_dict(invi_obj.user)
      i['phone'] = invi_obj.phone
      form = InvigilatorForm(initial=i)
      context['invi_id']=invi_obj.id
  if request.method == 'POST':
    if add:
      form = InvigilatorForm(request.POST)
      if form.is_valid():
        email = form.cleaned_data['email']
        phone=form.cleaned_data['phone']
        check_user = User.objects.filter(Q(email=email) | Q(username=email))
        if check_user:
          check_user_invi = Invigilator.objects.filter(user=check_user[0],vle=vle)
          if check_user_invi:
            messages.add_message(request,messages.ERROR,f'Invigilator with email {email} already exists in your account.No changes have been made.')
            return render(request,'csc/invigilator.html',context)
          else:
            invi=Invigilator.objects.create(user=check_user[0],phone=phone,vle=vle)
            messages.add_message(request,messages.INFO,f'User with email {email} already exists in the system & has been assigned to you as an invigilator.')
            return render(request,'csc/invigilator.html',context)
        
        u=form.save(commit=False)
        u.username = email
        u.save()
        invi=Invigilator.objects.create(user=u,phone=phone,vle=vle)
        messages.add_message(request,messages.SUCCESS,f'Invigilator with email {email} is added.')
    if edit:
      invi = request.POST.get('invi_id')
      invi_obj = Invigilator.objects.get(id=invi)
      context['invi_id']=invi_obj.id
      i = model_to_dict(invi_obj.user)
      i['phone'] = invi_obj.phone
      form = InvigilatorForm(request.POST,instance=invi_obj.user)
      if form.is_valid():
        u=form.save(commit=False)
        # u.username = form.cleaned_data['email']
        u.save()
        invi_obj.phone=form.cleaned_data['phone']
        invi_obj.save()
        messages.add_message(request,messages.SUCCESS,f'Invigilator details updated successfully.')
      else:
        print(f"\n\n 11 errors*********************\n{form.errors}")      
  context['form'] = form
  context['invigilator'] = form
  
  
    
    
  return render(request,'csc/invigilator.html',context)


def create_invigilatordelete_invigilator(request):
  data = {}
  try:
    
    invi=request.GET.get("invi")
    i=Invigilator.objects.get(id=invi)
    email = i.user.email
    i.delete()
    messages.add_message(request,messages.SUCCESS,f'Invigilator {email} deleted successfully.')
    data['status'] = 1
  except:
    data['status'] = 0
  # return redirect('/csc/invigilator')
  return JsonResponse(data)

# invigilator views

def create_invigilator(request):
  context ={}
  send_mail = False
  vle = VLE.objects.get(user=request.user)
  form = InvigilatorForm(request.POST or None)
  context['form'] = form
  if form.is_valid():
    email = form.cleaned_data['email']
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    phone = form.cleaned_data['phone']
    try:
      user = User.objects.get(email=email)
      messages.add_message(request,messages.SUCCESS,f'User with this email {email} already exists & assigned to you as an Invigilator.')
    except User.DoesNotExist:
      user = User.objects.create(username=email,email=email,first_name=first_name,last_name=last_name)
      send_mail = True
      messages.add_message(request,messages.SUCCESS,f'User email {email} is assigned to you as an Invigilator.')
    except User.MultipleObjectsReturned:
      user = User.objects.filter(email=email)[0]
      messages.add_message(request,messages.SUCCESS,f'User with this email {email} already exists & assigned to you as an Invigilator.')
    try:
      # Invigilator.objects.create(user=user,vle=vle,phone=phone)
      i=Invigilator.objects.create(user=user,phone=phone)
      i.vle.add(vle)
      invi_group = Group.objects.get(name='INVIGILATOR')
      invi_group.user_set.add(user)
      if send_mail:
        send_pwd_mail_to_invi(user)
    except IntegrityError:
      messages.add_message(request,messages.ERROR,f'User with this email {email} has already been assigned to you as an Invigilator.')
    except Exception as e:
      print(e)
  return render(request,'csc/create_invigilator.html',context)
  
def view_invigilators(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  invigilators = Invigilator.objects.filter(vle=vle)
  context['invigilators'] = invigilators
  return render(request,'csc/list_invigilators.html',context)

def update_invigilator(request,id):
  context = {}
  invi = get_object_or_404(Invigilator, id = id)
  # form = InvigilatorForm(request.POST or None)
  if request.method == 'GET':
    data = {'phone': invi.phone, 'first_name': invi.user.first_name,'last_name': invi.user.last_name,'email': invi.user.email}
    form = InvigilatorForm(initial=data)
    form.fields['email'].disabled = True 
    context['form']  = form
  else:
    
    
    form = InvigilatorForm(request.POST)
    if form.is_valid():
      phone = form.cleaned_data['phone']
      first_name = form.cleaned_data['first_name']
      last_name = form.cleaned_data['last_name']
      invi.phone = phone
      invi.save()
      user = invi.user
      user.first_name = first_name
      user.last_name = last_name
      user.save()
    else:
      print(f"4 error ****************************** {form.non_field_errors}")
    data = {'phone': invi.phone, 'first_name': invi.user.first_name,'last_name': invi.user.last_name,'email': invi.user.email}
    form = InvigilatorForm(initial=data)
    form.fields['email'].disabled = True 
    context['form']  = form
  return render(request,'csc/update_invigilator.html',context)

def delete_invigilator(request, id):
  context ={}
  obj = get_object_or_404(Invigilator, id = id)
  if request.method =="POST":
    obj.delete()
    return redirect('csc:view_invigilators')
  return render(request, "delete_view.html", context)

class InvigilatorDeleteView(DeleteView):
  model = Invigilator
  success_url ="/"
  template_name = "csc/invigilator_confirm_delete.html"
  

def invi_dashboard(request):
  context = {}
  invi = Invigilator.objects.get(user=request.user)
  upcoming_tests = Test.objects.filter(invigilator=invi,tdate__gte=datetime.datetime.today())
  completed_tests = Test.objects.filter(invigilator=invi,tdate__lt=datetime.datetime.today())
  context['upcoming_tests'] = upcoming_tests
  context['completed_tests'] = completed_tests
  return render(request,'csc/invigilator_dashboard.html',context)
  
  
# ajax functions
@csrf_exempt
def assign_foss(request):
  vle = VLE.objects.get(user=request.user)
  students = request.POST.getlist('student[]')
  fosses = request.POST.getlist('foss[]')
  f = FossCategory.objects.filter(foss__in=[x for x in fosses]).values_list('foss')
  foss_name = ', '.join([x[0] for x in f])
  for student in students:
    #check if student has individual
    for foss in fosses:
      try:
        f = FossCategory.objects.get(foss=foss)
        s = Student.objects.get(id=int(student))
        c = CertifiateCategories.objects.get(code='INDI')
        scc = Student_certificate_course.objects.get(student=s,cert_category=c)
        Student_Foss.objects.create(student=s,csc_foss=f,cert_category=scc.cert_category,foss_start_date=datetime.date.today())
      except Exception as e:
        print(e)
    
  return JsonResponse({'foss':foss_name,'student_count':len(students)})


@login_required
@is_vle
def download_certificate(request, test_attendance_id):
    test_attendance = get_object_or_404(CSCTestAtttendance, pk=test_attendance_id)

    details = get_details(test_attendance)
    filename = 'certficate.pdf'
    certificate = generate(**details)
    if not certificate[1]:
        add_log(details['certificate_pass'], test_attendance_id)
        return certificate[0]
    else:
        messages.error(request,"Problem in downloading!")
        return HttpResponse(certificate[0]) 


def get_details(test_attendance):
    t = test_attendance.test
    v = t.vle
    c = v.csc.csc_id
    details = {
        'test_date': test_attendance.test.tdate.strftime("%Y-%m-%d"),
        'tstudent':  test_attendance.student.user.get_full_name(),
        'foss': test_attendance.test.foss.foss,
        'institute': c,
        'score': '{0}'.format(round(test_attendance.mdlgrade, 2)),
        'certificate_pass': get_pass(test_attendance.id, t.id),
    }

    return details

def has_log_entry(key):
    return Log.objects.filter(key=key).exists()

def add_log(key, ta):
    if not has_log_entry(key):
       log = Log()
       log.key = key
       log.test_attendance_id = ta
       log.save()


def verify(request, key=None):
    context = {}
    ci = RequestContext(request)
    detail = None
    if key is not None:
        details = get_verification_details(key)
    elif request.method == 'POST':
        key = request.POST.get('key').strip()
        details = get_verification_details(key)
    return render_to_response('verify.html', {'details': details}, ci)

def get_verification_details(key):
    log = get_object_or_404(Log, key=key)
    ta = log.test_attendance
    details = get_details(ta)
    return details

def get_pass(ta_id, t_id):
    serial_key = (hashlib.sha1(bytes('{0}{1}'.format(ta_id, t_id), 'utf-8'))).hexdigest()
    return serial_key[0:10]


def training_enroll(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  students = [x.id for x in Student.objects.filter(vle_id=vle.id) ]
  sf = Student_Foss.objects.filter(student_id__in=students).values('student_id','student__user__email','csc_foss__foss','foss_start_date').annotate(fullname=Concat(F('student__user__first_name'),Value(' '),F('student__user__last_name')))
    
  
  
  
  context['sf']=sf
  return render(request,'csc/training_enroll.html',context)

def test_enroll(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  students = [x.id for x in Student.objects.filter(vle_id=vle.id) ]
  ta = CSCTestAtttendance.objects.filter(student_id__in=students).values('student_id','student__user__email','test__foss__foss','test__tdate','test__ttime','status','mdlgrade').annotate(fullname=Concat(F('student__user__first_name'),Value(' '),F('student__user__last_name')))
  context['ta']=ta
  return render(request,'csc/test_enroll.html',context)
  
  
def test_certi(request):
  context = {}
  vle = VLE.objects.get(user=request.user)
  students = [x.id for x in Student.objects.filter(vle_id=vle.id) ]
  ta = CSCTestAtttendance.objects.filter(student_id__in=students,mdlgrade__gte=PASS_GRADE).values('student_id','student__user__email','test__foss__foss','test__tdate','test__ttime','status','mdlgrade').annotate(fullname=Concat(F('student__user__first_name'),Value(' '),F('student__user__last_name')))
  context['ta']=ta
  return render(request,'csc/test_certi.html',context)
  
