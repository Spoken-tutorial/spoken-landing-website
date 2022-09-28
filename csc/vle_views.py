from django.db import IntegrityError
from django.template import context
from django.urls import reverse
from re import template
from django.contrib.auth.views import LoginView
from django.views.generic import *
from django.shortcuts import render
from .utils import *
from csc.models import *
from spokenlogin.models import *
from django.http import JsonResponse, request
from .vle_forms import *

from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import *

from django.views.generic.edit import CreateView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy

import logging


import string
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import F,ExpressionWrapper,Subquery,OuterRef,Exists,Q
from django.db.models.fields import BooleanField

from datetime import timedelta
from django.conf import settings
import requests
from .cron import add_vle,add_transaction

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

@csrf_exempt
def vle_dashboard(request):
    context = {}
    # user = request.user
    vle = VLE.objects.filter(user=request.user).first()

    context['vle'] = vle
    context['user'] = request.user
    
    context['upcoming_test_stats'] = get_upcoming_test_stats()
    context['courses_offered_stats'] = get_courses_offered_stats()
   
    # context['stats_dca'] = get_programme_stats('dca')
    # context['stats_individual'] = get_programme_stats('individual')

    context['total_students_enrolled'] = Student.objects.filter(vle_id=vle).count()
    context['total_tests_completed'] = Test.objects.filter(vle=vle,tdate__gte=datetime.datetime.today().date()).count()
    context['total_certificates_issued'] = StudentTest.objects.filter(status=4).count() #ToDo check condition
    
    # context['fosses_perc'] = get_foss_enroll_percent(vle)
    return render(request, 'csc/vle.html', context)
   

def courses(request):
  context = {}
  vles = VLE.objects.filter(user=request.user)
  for vle in vles:

    individual_foss = {}
    # for item in individual_csc_foss:
    #   students = Student_Foss.objects.filter(csc_foss=item.id).count()
    #   individual_foss[item.spoken_foss.foss] = {'total_students':students}


    fosses = FossCategory.objects.filter(available_for_jio=True)
    indi_students = Student_certificate_course.objects.filter(cert_category__code='INDI', student__in=Student.objects.filter(vle_id=vle.id)).values_list('student_id')
    
    for item in fosses:
      students = Student_Foss.objects.filter(csc_foss=item.id, student__in=indi_students).count()
      individual_foss[item.foss] = {'total_students':students}

    context['individual_foss'] = individual_foss
  return render(request,'csc/courses.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class GetFossOptionView(JSONResponseMixin, View):
  def dispatch(self, *args, **kwargs):
    return super(GetFossOptionView, self).dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
    programme_type = self.request.POST.get('programme_type')
    print(programme_type,"*****************")
    context = {}

    foss_option = "<option value=''>---------</option>"


    if programme_type == 'dca':
        fosses = FossCategory.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
    else:
        fosses = FossCategory.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')

    for foss in fosses:
      foss_option += "<option value=" + str(foss.id) + ">" + str(foss.foss) + "</option>"

    print(foss_option)
    context = {
      'spoken_foss_option' : foss_option,
    }
    return self.render_to_json_response(context)


@is_vle
def student_list(request):
  context={}
  vle = VLE.objects.filter(user=request.user).first()
  students = []
  search = False
  course = request.GET.get('course')
  foss = request.GET.get('foss')
  name = request.GET.get('name')
  dates = request.GET.get('dates')
  print(f"\n\n{request.GET}")
  print(f"{course},{foss},{name},{dates}")
  
    
  
  findividual = FossCategory.objects.filter(available_for_jio=True)
  # findividual = FossCategory.objects.filter(programme_type='individual',vle=vle)


  context['foss_individual'] = [x for x in findividual]
  # context['foss_individual'] = findividual
  # for vle in vles:
  # s = Student.objects.filter(vle_id=vle.id)
  indi_id = CertifiateCategories.objects.get(code="INDI").id
  indi_course = Student_certificate_course.objects.filter(student_id=OuterRef('id'),cert_category_id=indi_id)
  s = Student.objects.filter(vle_id=vle.id).annotate(indi=Exists(indi_course))
  print(s.query)
  # all_students = Student.objects.filter(vle_id=vle.id)
  if name:
    print(f"\n name")
    s = s.filter(Q(user__first_name__icontains=name)|Q(user__last_name__icontains=name)|Q(user__email__icontains=name))
  if course:
    print(f"\n course - {course}")
    if CertifiateCategories.objects.get(id=course).code == 'INDI':
      context['is_indi'] = True
    try:
      s = s.filter(id__in=[x.student.id for x in Student_certificate_course.objects.filter(cert_category__id=course)])
    except Exception as e:
      print(e)
      print(f"course except")
  if foss:
    print(f"\n foss")
    try:
      s = s.filter(id__in=[Student_Foss.objects.get(id=foss)])
    except:
      print(f"foss except")
  if not (course or foss or name):
    context['is_indi'] = True
    
  # if dates:
  #   print(f"\n dates")
  #   start = dates.split('-')[0].strip()
  #   end = dates.split('-')[0].strip()
  #   print(f"\n\n\n\nstart - {start}, end - {end}")
    
  
    
  #   if start==end:
  #     print("\n\n equal dates")
  #     start_date = datetime.datetime.strptime(start, '%m/%d/%Y')
  #     start_date = start_date.date()
  #     s = s.filter(date_of_registration=start_date)
  #   else:
  #     start_date = datetime.datetime.strptime(start, '%m/%d/%Y').date()
  #     end_date = datetime.datetime.strptime(start, '%m/%d/%Y').date()
      
  #     print("\n\n not equal dates")
  #     s = s.filter(date_of_registration__gte=start,date_of_registration_lte=end_date)
      
  print(f"\n\ns - {s}\n\n")
  for item in s:
    # print(type(item.indi))
    if item.indi:
      # print(item.id)
      pass
    students.append(item)
  context['students'] = students
  context['students'] = s
  # print(f"\ncontext['students']")
  # print(f"{context['students']}")
  vle_courses = Student_certificate_course.objects.filter(student__in=s)
  distinct_courses = set()
  for item in vle_courses:
    # print(item.cert_category)
    distinct_courses.add(item.cert_category)
  context['distinct_courses'] = distinct_courses
  vle_fosses = Student_Foss.objects.filter(student__in=s)
  # print(f"\n\nvle_fosses *** {vle_fosses}\n\n")
  distinct_foss = set()
  for item in vle_fosses:
    distinct_foss.add(item.csc_foss)
  l = list(distinct_foss)
  l.sort(key=lambda x: x.foss.title())
  context['distinct_foss'] = l
  # print(f"distinct_courses ******* {distinct_courses}")
  return render(request,'csc/students_list.html',context)

@csrf_exempt
def assign_foss(request):
  print(f"\n\nPOST******************************************")
  print(request.POST)
  vle = VLE.objects.get(user=request.user)
  students = request.POST.getlist('student[]')
  
  fosses = request.POST.getlist('foss[]')
  

  # f = FossCategory.objects.filter(id__in=[int(x) for x in fosses]).values_list('foss')
  f = FossCategory.objects.filter(foss__in=[x for x in fosses]).values_list('foss')
  foss_name = ', '.join([x[0] for x in f])
  for student in students:
    #check if student has individual
    for foss in fosses:
      print(f"foss in for ***** {foss}\n")
      try:
        f = FossCategory.objects.get(foss=foss)
        s = Student.objects.get(id=int(student))
        c = CertifiateCategories.objects.get(code='INDI')
        scc = Student_certificate_course.objects.get(student=s,cert_category=c)
        Student_Foss.objects.create(student=s,csc_foss=f,csc_cert_course=scc)
      except Exception as e:
        print(e)
    
  return JsonResponse({'foss':foss_name,'student_count':len(students)})


def student_profile(request,id):
  context={}
  student = Student.objects.get(id=id)
  initial={'fname': student.user.first_name , 'lname': student.user.last_name, 'state' :student.state}
  form = StudentForm(instance=student,initial=initial)
  context['form'] = form
  if request.method == 'POST':
    initial={'fname': student.user.first_name , 'lname': student.user.last_name,'state':student.state}
    form = StudentForm(request.POST,instance=student,initial=initial)
    if form.is_valid():
      user = User.objects.get(email=student.user.email)
      user.first_name = form.cleaned_data['fname']
      user.last_name = form.cleaned_data['lname']
      user.save()
      form.save()
      messages.add_message(request, messages.SUCCESS, 'Student data updated. Refresh for viewing updated data.')
  
  dca_foss = []
  individual_foss = []
  
  stu_cat_foss ={} #students cert-category and fosses dict

  
  #certificate packages taken by students
  s_categories = Student_certificate_course.objects.filter(student=student)
  
  for s_cat in s_categories:
    print("_______________________")
    print(s_cat.cert_category)
    print("_______________________")

    if s_cat.cert_category.code=="INDI":
      #indi code
      cat_fosses = FossCategory.objects.filter(
        id__in=Student_Foss.objects.filter(cert_category=s_cat.cert_category).values_list('csc_foss'))
    else:

      cat_fosses = FossCategory.objects.filter(
        id__in=CategoryCourses.objects.filter(certificate_category=s_cat.cert_category).values_list('foss')
        )
    s_fosses=[] #list fosses in category
    for cf in cat_fosses:

      print(cf.foss)
      s_fosses.append(cf.foss)
      print("******")
      print(s_fosses)


    stu_cat_foss[(s_cat.cert_category.code+" - "+s_cat.cert_category.title)]=s_fosses

  print(stu_cat_foss,"########################")
 

  context['s_categories'] = s_categories
  context['stu_cat_foss'] = stu_cat_foss
  
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


# class TestCreateView(CreateView):
#   model = Test
#   fields = '__all__'
  
#   def get_form(self, *args, **kwargs):
#     form = super(TestCreateView, self).get_form(*args, **kwargs)
#     vle = VLE.objects.filter(user=self.request.user).first()
#     vle_foss = Vle_csc_foss.objects.filter(vle=vle)
#     fosses = FossCategory.objects.filter(id__in=[x.spoken_foss.id for x in vle_foss])
#     form.fields['foss'].queryset = fosses
#     return form

#   def get_success_url(self):
#     # return self.get_absolute_url()
#     return '/'

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
  fields = ['test_name','foss','tdate','ttime','note_student','note_invigilator','publish']
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
    print(form)

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
  fields = ('test_name','foss', 'tdate', 'ttime', 'note_student', 'note_invigilator', 'publish' )
  

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
      print(f"t ------ {t}")
      form.fields['ttime'].initial = t
      return form

  def get_context_data(self, **kwargs):
    print(f"1 **".ljust(50,'-'))
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
    print(f"test - {test}")
    print(f"students ---- {students}")
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

@csrf_exempt
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
  print("4 ------- ")
  data['upcoming_tests'] = get_upcoming_test_stats()
  print("5 ------- ")
  data['course_type_offered'] = get_courses_offered_stats()
  print("6 ------- ")
  data['course_count_result'] = get_programme_stats()
  print("7 ------- ")
  
  return JsonResponse(data)

def mark_attendance(request,id):
  context = {}
 
  test = Test.objects.get(id=id)
  # st = [x.student for x in StudentTest.objects.filter(test=test)]
  st = StudentTest.objects.filter(test=test)
  context['test'] = test
  context['students'] = st
  total_enrolled = len(st)
  attending = StudentTest.objects.filter(test_status=1).count()
  pending = total_enrolled - attending
  context['total_enrolled'] = total_enrolled
  context['attending'] = attending
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