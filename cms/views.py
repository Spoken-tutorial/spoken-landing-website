from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import District,City
from django.http import JsonResponse
from django.views.generic.edit import CreateView
# Create your views here.
@csrf_exempt
def load_district(request):
  id = request.POST.get('id',0)
  districts = District.objects.filter(state_id=id).values('id','name')
  district_lst = [item for item in districts]
  data = {'districts':district_lst}
  return JsonResponse(data)

@csrf_exempt
def load_city(request):
  id = request.POST.get('id',0)
  cities = City.objects.filter(state_id=id).values('id','name')
  data = {'cities':list(cities)}
  return JsonResponse(data)

