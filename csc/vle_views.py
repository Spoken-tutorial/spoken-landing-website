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

import string
import random
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

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
    
    context['upcoming_test_stats'] = get_upcoming_test_stats()
    context['courses_offered_stats'] = get_courses_offered_stats()
   
    context['stats_dca'] = get_programme_stats('dca')
    context['stats_individual'] = get_programme_stats('individual')

    context['total_students_enrolled'] = Student.objects.filter(vle_id=vle).count()
    context['total_tests_completed'] = Test.objects.filter(vle=vle,tdate__gte=datetime.datetime.today().date()).count()
    context['total_certificates_issued'] = StudentTest.objects.filter(status=4).count() #ToDo check condition
    
    context['fosses_perc'] = get_foss_enroll_percent(vle)
    if request.method == 'POST':
        form = form = FossForm(request.POST)
        if form.is_valid():
            programme_type = form.cleaned_data['programme_type']
            spoken_foss = form.cleaned_data['spoken_foss']
            vle = VLE.objects.filter(user=request.user).first()
            for sf in spoken_foss:
                #check if fossid already exist
                vfoss=Vle_csc_foss()

                vfoss.programme_type=programme_type
                # vfoss.spoken_foss=sf.id
                vfoss.spoken_foss=sf
                vfoss.vle=vle
                try:
                    vfoss.save()
                    messages.success(request, sf.foss+" has been added.")
                except Exception as e:
                    print(f"exceptioon - {e}")
                    messages.error(request, "Records already present.")
            
            return HttpResponseRedirect("/csc/vle/")
        
        context = {'form':form}
        return render(request, 'csc/vle.html', context)
    else:
        context.update(csrf(request))
        added_foss = Vle_csc_foss.objects.all()
        
        foss_form = FossForm()
        context['form']=foss_form
        context['added_foss']=added_foss
        return render(request, 'csc/vle.html',context)

def courses(request):
  context = {}
  vles = VLE.objects.filter(user=request.user)
  for vle in vles:
    dca_csc_foss = Vle_csc_foss.objects.filter(vle=vle,programme_type='dca')
    individual_csc_foss = Vle_csc_foss.objects.filter(vle=vle,programme_type='individual')
    dca_foss = {}
    for item in dca_csc_foss:
      students = Student_Foss.objects.filter(csc_foss=item.id).count()      
      dca_foss[item.spoken_foss.foss] = {'total_students':students}

    individual_foss = {}
    for item in individual_csc_foss:
      students = Student_Foss.objects.filter(csc_foss=item.id).count()
      individual_foss[item.spoken_foss.foss] = {'total_students':students}

    context['dca_foss'] = dca_foss
    context['individual_foss'] = individual_foss

  if request.method == 'POST':
    form = form = FossForm(request.POST)
    if form.is_valid():
        programme_type = form.cleaned_data['programme_type']
        spoken_foss = form.cleaned_data['spoken_foss']
        vle = VLE.objects.filter(user=request.user).first()
        for sf in spoken_foss:
            #check if fossid already exist
            vfoss=Vle_csc_foss()

            vfoss.programme_type=programme_type
            # vfoss.spoken_foss=sf.id
            vfoss.spoken_foss=sf
            vfoss.vle=vle
            try:
                vfoss.save()
                messages.success(request, sf.foss+" has been added.")
            except Exception as e:
                print(f"exceptioon - {e}")
                messages.error(request, "Records already present.")
    
    context['form'] = form
    # return HttpResponseRedirect("/csc/courses/")
    return render(request, 'csc/courses.html', context)
  else:
    form = FossForm()
        # context['form']=foss_form
    context['form'] = form
    return render(request, 'csc/courses.html', context)
        


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
  # dca = Vle_csc_foss.objects.filter(programme_type='dca').values_list('spoken_foss')
  # individual = Vle_csc_foss.objects.filter(programme_type='individual').values_list('spoken_foss')
  # fdca = SpokenFoss.objects.filter(id__in=[x[0] for x in dca])
  # fdca = SpokenFoss.objects.filter(id__in=[x[0] for x in dca])
  # findividual = SpokenFoss.objects.filter(id__in=[x[0] for x in individual])
  # findividual = SpokenFoss.objects.filter(id__in=[x[0] for x in individual])
  fdca = Vle_csc_foss.objects.filter(programme_type='dca',vle=vle)
  findividual = Vle_csc_foss.objects.filter(programme_type='individual',vle=vle)
  context['foss_dca'] = [x.spoken_foss for x in fdca]
  context['foss_individual'] = [x.spoken_foss for x in findividual]
  # context['foss_individual'] = findividual
  # for vle in vles:
  s = Student.objects.filter(vle_id=vle.id)
  for item in s:
    students.append(item)
  context['students'] = students
  return render(request,'csc/students_list.html',context)

@csrf_exempt
def assign_foss(request):
  print(request.POST)
  vle = VLE.objects.get(user=request.user)
  students = request.POST.getlist('student[]')
  fosses = request.POST.getlist('foss[]')
  f = FossCategory.objects.filter(id__in=[int(x) for x in fosses]).values_list('foss')
  foss_name = ', '.join([x[0] for x in f])
  
  print(f"students".ljust(40,'*')+f"students")
  print(f"foss".ljust(40,'*')+f"foss")
  for student in students:
    for foss in fosses:
      try:
        f = Vle_csc_foss.objects.get(spoken_foss=int(foss),vle=vle)
        s = Student.objects.get(id=int(student))
        Student_Foss.objects.create(student=s,csc_foss=f)
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
  sf = Student_Foss.objects.filter(student=student)
  for item in sf:
    if item.csc_foss.programme_type == 'dca':
      dca_foss.append(item.csc_foss.spoken_foss)
    else:
      individual_foss.append(item.csc_foss.spoken_foss)

  context['dca_foss'] = dca_foss
  context['individual_foss'] = individual_foss
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
    page = self.request.GET.get('page')
    paginator = Paginator(tests, self.paginate_by)
    try:
      tests = paginator.page(page)
    except PageNotAnInteger:
      tests = paginator.page(1)
    except EmptyPage:
      tests = paginator.page(paginator.num_pages)
    context['tests'] = tests
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


def invigilator_profile(request):
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
  return render(request,'csc/invigilator_profile.html',context)

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
  return HttpResponseRedirect(reverse('csc:invigilator_profile') )

def get_stats(request):
  data = {}
  print("4 ------- ")
  data['upcoming_tests'] = get_upcoming_test_stats()
  print("5 ------- ")
  data['course_type_offered'] = get_courses_offered_stats()
  print("6 ------- ")
  data['dca_students'] = get_programme_stats('dca')
  print("7 ------- ")
  data['individual_students'] = get_programme_stats('individual')
  print("8 ------- ")
  
  return JsonResponse(data)