
from urllib import request
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from .models import VLE, CSC
from datetime import datetime as dt 
from datetime import timedelta
import requests
from django.conf import settings
from .cron import add_vle,add_transaction
from django.contrib import messages

class CSCBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            pwd_exists = user.password
            if pwd_exists:
                pwd_valid = check_password(password, pwd_exists)
                if pwd_valid:
                    return user

        except:
            user = check_updated_vle(username,request)
            return user
        return None


def check_updated_vle(username,request):
    last_update_date = VLE.objects.order_by('user__date_joined').last().user.date_joined
    delta_date = last_update_date - timedelta(2)
    payload = {'date':delta_date}
    url = getattr(settings, "URL_FETCH_VLE", "http://exam.cscacademy.org/shareiitbombayspokentutorial")
    response = requests.get(url,params=payload)
    if response.status_code == 200:
        data = response.json()
    data = data['req_data']
    emails = [x['email'] for x in data]

    for item in data:
        if username == item['email']:
            try:
                csc = CSC.objects.get(csc_id=item['csc_id'])
            except CSC.DoesNotExist:
                print(f"csc - {item['csc_id']} does not exists")
                CSC.objects.create(
                    csc_id=item.get('csc_id'),institute=item.get('institute',''),state=item.get('state',''),
                    city=item.get('city',''),district=item.get('district',''),block=item.get('block',''),
                    address=item.get('address',''),pincode=item.get('pincode',''),plan=item.get('plan',''),
                    activation_status=1
                )
                csc = CSC.objects.get(csc_id=item.get('csc_id'))
            add_vle(item,csc)
            vle = VLE.objects.get(user__email=username)
            add_transaction(vle,csc,item['transcdate'])
            # messages.add_message(request,messages.INFO,'hello')
            return vle.user
    else: 
        # messages.add_message(request,messages.INFO,'hello')
        return None
