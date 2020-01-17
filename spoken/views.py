from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Products, Nav, Blended_workshops
from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')


def index(request):
    return HttpResponse("Hello, world. You're at the spoken landing page.")

def home(request):
    # return HttpResponse("Hello, world. You're at the spoken landing page.")
    navs = Nav.objects.filter(status=1)
    products = Products.objects.all()
    workshops = Blended_workshops.objects.filter(workshop_date__gte=today).order_by('-workshop_date')[:5]
    context = {
    'product_list':products,
    'nav_list': navs,
    'workshops': workshops
    }
    return render(request, 'spoken/home.html', context)
