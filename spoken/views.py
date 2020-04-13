from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
from django.http import HttpResponse
from .models import Products, Nav, Blended_workshops, Jobfair, Internship, Testimonials, MediaTestimonials, Award
from datetime import datetime
from django.utils import timezone
from .forms import ContactForm
from django.contrib import messages

today = datetime.today().strftime('%Y-%m-%d')

def home(request):
    if request.method == 'POST':
        c = ContactForm(request.POST)
        if c.is_valid():
            c.save()
            messages.add_message(request,messages.INFO,'Message submitted!')
            return redirect('/spoken#contact')
            #c = ContactForm()
    else:
        c = ContactForm()

    # return HttpResponse("Hello, world. You're at the spoken landing page.")
    navs = Nav.objects.filter(status=1)
    products = Products.objects.all()
    now = timezone.now()
    jobfairs = Jobfair.objects.all().order_by('-jobfair_start_date')[:3]
    internships = Internship.objects.all().order_by('-internship_start_date')[:3]
    workshops = Blended_workshops.objects.all().order_by('-workshop_start_date')[:3]
    testimonials = Testimonials.objects.all()[:9]
    media_testimonials = MediaTestimonials.objects.all()[:3]
    awards = Award.objects.all().order_by('order');
    context = {'jobfairs':jobfairs,'internships':internships,'workshops':workshops,'products':products, 
    'nav_list':navs, 'form':c, 'testimonials':testimonials,'media_testimonials':media_testimonials,'media_url' : settings.MEDIA_URL,
    'awards':awards,}

    return render(request,'spoken/home.html',context)
