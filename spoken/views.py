from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse
from .models import Products, Nav, Blended_workshops, Jobfair, Internship
from datetime import datetime
from django.utils import timezone
from .forms import ContactForm

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
    jobfairs = Jobfair.objects.filter(jobfair_date__gte=now).order_by('jobfair_date')[:3]
    internships = Internship.objects.filter(internship_date__gte=now).order_by('internship_date')[:2]
    workshops = Blended_workshops.objects.filter(workshop_date__gte=now).order_by('workshop_date')[:3]
    context = {'jobfairs':jobfairs,'internships':internships,'workshops':workshops,'products':products, 'nav_list':navs}

    return render(request,'spoken/home.html',context)
