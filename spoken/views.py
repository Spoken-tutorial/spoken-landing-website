from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
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
import os
from dotenv import load_dotenv
import pymongo
from spokenlogin.models import SpokenUser
from django.contrib.auth.models import User
from django.db.models import Count
from .mat_rec import TutorialRecommender
from collections import defaultdict
import pickle
import numpy as np
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
        sc = get_supercategory(courseProgress,get_jobs(request))
        context['supercategory'] = sc
        context = merge_two_dicts(matrix_factorization(request), context)
    return render(request,'spoken/dashboard.html',context)

# Put this inside cron
def update_progress(request):
    context = {}
    # Mongo DB user Upgrade
    try:
        d = requests.get('https://spoken-tutorial.org/api/get_users_progress/').json()
        '''
        Username:   [   [ 0-FOSS, 1-Tutorial, 2-Language, 3-Video played till
                        4-Tutorial total time, 5-Total tutorials ]
                    ]
        '''
        all_same_fosses = True
        for key,values in d.items():
            curr_foss = values[0][0]
            prev_tutorial = values[0][1]
            try:
                spuser = SpokenUser.objects.get(username=key)
                user = User.objects.get_or_create(email=spuser.email)
                print('User exists',user)
                if user[1]:
                    user[0].username=spuser.username,
                    user[0].first_name=spuser.first_name,
                    user[0].last_name=spuser.last_name
                    user[0].save()
                for a_list in values:
                    if curr_foss == a_list[0]:
                        if prev_tutorial != a_list[1]:
                            prev_tutorial = a_list[1]
                            tp = TutorialProgress.objects.get_or_create(
                                foss=a_list[0],
                                tutorial = a_list[1],
                                language=a_list[2],
                                total_duration=abs(int(a_list[4])),
                                user=user[0]
                                )
                            if tp[0].time_completed < abs(int(a_list[3])):
                               tp[0].time_completed = abs(int(a_list[3]))
                               tp[0].save()
                    else:
                        cp =CourseProgress.objects.get_or_create(
                            foss=a_list[0],
                            language=a_list[2],
                            total_tutorials=a_list[5],
                            user=user[0])
                        count = TutorialProgress.objects.filter(
                            foss=curr_foss, language = a_list[2],
                            user = user[0]).count()
                        if cp[0].tutorials_completed < count:
                            cp[0].tutorials_completed = count
                            cp[0].save()
                        all_same_fosses = False
                        curr_foss = a_list[0]
                if all_same_fosses:
                    cp =CourseProgress.objects.get_or_create(
                        foss=a_list[0],
                        language=a_list[2],
                        total_tutorials=a_list[5],
                        user=user[0])
                    count = TutorialProgress.objects.filter(
                            foss=curr_foss, language = a_list[2],
                            user = user[0]).count()
                    if cp[0].tutorials_completed < count:
                            cp[0].tutorials_completed = count
                            cp[0].save()
            except Exception as e:
                print("Uknown user",e)
    except:
        print('improper JSON - skipping to next')
    print('Updated')
    return HttpResponseRedirect('/')

# importing copy module
import copy

def matrix_factorization(request):
    context ={}
    tut_prog = TutorialProgress.objects.all()
    tuts = list(tut_prog.values_list('tutorial','foss').distinct())
    t = list(tut_prog.values_list('tutorial').distinct())
    datas = tut_prog.values_list('user','tutorial',
        ).order_by('user')
    tutorial_matrix = []
    prev_user = 0
    user_dict = {}
    latent_tutorial_dict = {}
    latent_tutorial_matrix = [[0]*len(tuts)]*len(tuts)
    #make counter of tutorials
    for user, tutorial in datas:
        if user in user_dict:
            user_dict[user].append(tutorial)
        else:
            user_dict[user] = [tutorial]
    user_tut_dict = {}
    for user, tutorial_data in user_dict.items():
        temp = [0]*len(tuts)
        for tutorial in tutorial_data:
            for i in range(len(tuts)):
                if tuts[i][0] == tutorial:
                    temp[i] = 1
                else:
                    if not temp[i]:
                        temp[i] = 0
            if tutorial in latent_tutorial_dict:
                latent_tutorial_dict[tutorial] +=1
            else:
                latent_tutorial_dict[tutorial] = 1
        tutorial_matrix.append(temp)
        user_tut_dict[user] = temp
        for tut_key in latent_tutorial_dict:
            for t , f in enumerate(tuts):
                if latent_tutorial_dict[tut_key] == f[0]:
                    latent_tutorial_matrix[t] = latent_tutorial_dict[tut_key]
    ltm_normalized = []
    for i in range(len(latent_tutorial_matrix)):
        ltm_normalized.append(np.array(softmax(latent_tutorial_matrix[i])))
    try:
        model = pickle.load(open('good_model.pkl', 'rb'))
    except FileNotFoundError:
        model = train(tutorial_matrix,ltm_normalized,len(tuts))

    d = json.loads(requests.get('https://spoken-tutorial.org/api/get_top_tuts_foss/').json())
    context['top_tutorials'] = d['top_tutorials'][:5]
    context['top_fosses'] = d['top_foss'][:5]
    if request.user.id in user_tut_dict:
        try:
            pred = model.predict_user(user_tut_dict[request.user.id])
        except:
            model = train(tutorial_matrix,ltm_normalized,len(tuts))
            print('new pred')
            pred = model.predict_user(user_tut_dict[request.user.id])

        list_pred = list(pred)
        pred_index = list_pred.index(max(list_pred))
        user_at_that_index = user_tut_dict[request.user.id][pred_index]
        while ( user_at_that_index) :
            list_pred[pred_index] = -1
            pred_index = list_pred.index(max(list_pred))
            user_at_that_index = user_tut_dict[request.user.id][pred_index]
        t = tuts[pred_index]
        context['watch_next'] = t
    else:
        context['watch_next'] = d['top_tutorials'][0]

    return context

def train(tutorial_matrix,ltm_normalized, len_tuts):
    model = TutorialRecommender()
    model.fit(tutorial_matrix,ltm_normalized,len_tuts)
    with open('good_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    return model

def softmax(x):
    e_x = np.exp(x)
    return e_x / e_x.sum(axis=0)

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z