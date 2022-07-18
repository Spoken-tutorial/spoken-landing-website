import email
from django.template import context
from django.urls import reverse
from re import template
from django.contrib.auth.views import LoginView
from django.views.generic import *
from django.shortcuts import render
from .utils import *
from csc.models import *
from spokenlogin.models import *
from django.http import JsonResponse
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
    user = request.user

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
  vles = VLE.objects.filter(user=request.user)
  students = []
  dca = Vle_csc_foss.objects.filter(programme_type='dca').values_list('spoken_foss')
  individual = Vle_csc_foss.objects.filter(programme_type='individual').values_list('spoken_foss')
  fdca = SpokenFoss.objects.filter(id__in=[x[0] for x in dca])
  findividual = SpokenFoss.objects.filter(id__in=[x[0] for x in individual])
  context['foss_dca'] = fdca
  context['foss_individual'] = findividual
  for vle in vles:
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
  f = SpokenFoss.objects.filter(id__in=[int(x) for x in fosses]).values_list('foss')
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

  return render(request,'csc/courses.html',context)


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
