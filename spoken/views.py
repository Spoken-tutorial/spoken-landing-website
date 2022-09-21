from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import ContactMsg, Products, Nav, Blended_workshops, Jobfair, Internship, Testimonials, MediaTestimonials, Award
from django_ers.models import *
from datetime import datetime
from django.utils import timezone
from .forms import ContactForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import JobFairSerializer
from django.contrib import messages
import urllib, json
from django.views.generic import TemplateView
from .utils import *
from logs.models import TutorialProgress,CourseProgress
from logs.views import get_set_tutorial_progress
from django.core.mail import send_mail
from django.conf import settings


today = datetime.today().strftime('%Y-%m-%d')

def home(request):
    if request.method == 'POST':
        c = ContactForm(request.POST)
        if c.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values ={
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
                }
            data = urllib.parse.urlencode(values).encode()
            req =  urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
            is_spam = False
            emails = ContactMsg.objects.filter(email=c.cleaned_data['email'])
            if len(emails) > int(getattr(settings, "SPAM_EMAIL", 4)):
                is_spam = True 
            if result['success'] and not is_spam:
                c.save()
                try:
                    from_mail = settings.CONTACT_MAIL
                    to_mail = [settings.CONTACT_MAIL]
                    sub = 'spoken-tutorial.in feedback form'
                    name = c.cleaned_data['name']
                    email = c.cleaned_data['email']
                    subject = c.cleaned_data['subject']
                    message = c.cleaned_data['message']
                    mail_body = 'Name : ' + name +'\n' + 'Email : ' + email + '\n' + 'subject : '+ subject+ '\n'+'message : ' + message
                    send_mail(sub,mail_body,from_mail,to_mail,fail_silently=False,)
                    messages.add_message(request,messages.INFO,'Message submitted!')
                except Exception as e:
                    print(e)
                    messages.error(request, 'Some error occured.Please try again.')
                
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
            return redirect('/spoken#contact')
            #c = ContactForm()
    else:
        c = ContactForm()

    # return HttpResponse("Hello, world. You're at the spoken landing page.")
    group = [x.name for x in request.user.groups.all()]
    if 'VLE' in group:
        return HttpResponseRedirect(reverse('csc:vle_dashboard'))
    if 'STUDENT' in group:
        return HttpResponseRedirect(reverse('csc:student_dashboard'))
    navs = Nav.objects.filter(status=1)
    products = Products.objects.all().order_by('order')
    now = timezone.now()
    # jobfairs = Jobfair.objects.all().order_by('-jobfair_start_date')[:3]
    jobfairs = Event.objects.filter(type='JOB').order_by('-start_date')[:3]
    print('*************************', jobfairs)
    internships = Event.objects.filter(type='INTERN').order_by('-start_date')[:3]
    workshops = Blended_workshops.objects.all().order_by('-workshop_start_date')[:3]
    testimonials = Testimonials.objects.all()[:9]
    media_testimonials = MediaTestimonials.objects.all()[:3]
    awards = Award.objects.all().order_by('order');
    context = {'jobfairs':jobfairs,'internships':internships,'workshops':workshops,'products':products, 
    'nav_list':navs, 'form':c, 'testimonials':testimonials,'media_testimonials':media_testimonials,'media_url' : settings.MEDIA_URL,
    'awards':awards,}

    context['SITE_KEY'] = settings.GOOGLE_RECAPTCHA_SITE_KEY
    return render(request,'spoken/home.html',context)

#api/jobfairs/
class JobFairList(APIView):
    swagger_schema = None
    def get(self,request):
        # jobfairs = Jobfair.objects.all()
        jobfairs = Event.objects.filter(type='JOB')
        serializer = JobFairSerializer(jobfairs,many=True)
        return Response(serializer.data)


    def post(self):
        pass

def jobfairs(request):
    d = datetime.now()
    current_year = d.year
    context = {'current_year':current_year}
    return render(request,'spoken/jobfairs.html',context)

def jobfair_detail(request,jobfair_id):
    jobfair_obj = Jobfair.objects.filter(jobfair_id=jobfair_id)[0]
    context = {'jobfair_id':jobfair_id,'jobfair':jobfair_obj}
    return render(request,'spoken/jobfair_detail.html',context)


class TutorialSearch(TemplateView):
    """Search tutorial based on get url parameters. 
    Parameters: (search_foss, search_language)
    Example pattern: localhost:8000/spoken/tutorial-search/?search_foss=Advance+C&search_language=English
    """
    template_name = 'spoken/tutorial_search.html'
    
def dashboard(request):
    context = {}
    if request.user.is_authenticated:
        courseProgress = CourseProgress.objects.all().filter(user=request.user)
        context['courseProgress']=courseProgress
    return render(request,'spoken/dashboard.html',context)

