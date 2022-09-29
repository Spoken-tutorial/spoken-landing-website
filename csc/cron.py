from datetime import datetime
from django.db import IntegrityError
import requests
from django.conf import settings
from csc.models import VLE, Transaction
from django.contrib.auth.models import User
import string
import random
from django.contrib.auth.hashers import make_password
from .models import CSC
from django.db.models import Q
# import utils as u
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from .utils import get_tenure_end_date

def update_vle_data(): #CRON TASK
    url = getattr(settings, "URL_FETCH_VLE", "http://exam.cscacademy.org/shareiitbombayspokentutorial")
    print(f"url - {url}")
    response = requests.get(url)
    print(f"status : {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(1)
        updated = []
        vle_created = []
        csc_created = []
        count = 0
        # csc = [ csc[0] for csc in CSC.objects.values_list('id')]
        if data:
            data = data['req_data']
            for item in data :
                count+=1
                print(f"{item.get('email')}")
                update_flag = 0 
                try:
                    csc = CSC.objects.get(csc_id=item['csc_id'])
                    print(f"csc - {csc.csc_id} exists")
                    try:
                        vle=VLE.objects.get(csc__csc_id=item['csc_id'],user__email=item['email'])
                        print(f"vle - {vle.id}  exists")
                        # transactions = vle.transaction_set.all()
                        # transaction_dates = [ x.transcdate for x in transactions ]
                        # latest_transcdatest = max(transaction_dates)
                        # c = datetime.datetime.fromisoformat(item['transcdate'].split()[0]).date()
                        user = User.objects.get(id=vle.user.id)
                        if user.first_name != getFirstName(item['name']): 
                            vle.user.first_name = getFirstName(item['name'])
                            update_flag = 1
                        if user.last_name != getLastName(item['name']): 
                            vle.user.last_name = getLastName(item['name'])
                            update_flag = 2
                        if vle.phone != item['phone']: 
                            vle.phone = item['phone']
                            update_flag = 3
                        vle.save()
                        add_transaction(vle,csc,item['transcdate'])
                        if update_flag:
                            updated.append(f"{item['csc_id']} ({item['email']}) - {update_flag}")
                    except VLE.DoesNotExist:
                        print(f"vle - {item['email']}  does not exists")
                        add_vle(item,csc)
                        vle_created.append(f"{item['csc_id']} ({item['email']})")
                except CSC.DoesNotExist:
                    print(f"csc - {item['csc_id']} does not exists")
                    CSC.objects.create(
                        csc_id=item.get('csc_id'),institute=item.get('institute',''),state=item.get('state',''),
                        city=item.get('city',''),district=item.get('district',''),block=item.get('block',''),
                        address=item.get('address',''),pincode=item.get('pincode',''),plan=item.get('plan',''),
                        activation_status=1
                    )
                    csc = CSC.objects.get(csc_id=item.get('csc_id'))
                    print(f"csc - {item['csc_id']} created")
                    csc_created.append(f"{item['csc_id']} ({item['email']})")
                    add_vle(item,csc)
                    vle_created.append(f"{item['csc_id']} ({item['email']})")
        updated_str = ', '.join(updated)
        vle_created_str = ', '.join(vle_created)
        csc_created_str = ', '.join(csc_created)
        message = f"""
            CSC Data Updated : 
            Updated VLE Data : {len(updated)} - {updated_str}
            New VLEs created : {len(vle_created)} - {vle_created_str}
            New CSC created : {len(csc_created)} - {csc_created_str}
        """      
        send_log_mail(message)

# HELPER FUNCTIONS ----------------------------------------------------------------------------------------------------------------------------------
def send_password_mail(user,password):
    subject = "Login credentials for Spoken Tutorial :"
    from_email = getattr(settings, "NO_REPLY_MAIL", "no-reply@spoken-tutorial.org")
    to_email = user.email
    message = """
        Your login information for Spoken Tutorial is :
        username : {to_email}
        password : {password}
        Login link : "https://spoken-tutorial.in/login/"

        Best Wishes,
        Admin
        Spoken Tutorials
        IIT Bombay.
    """
    try:
        print(f"sending mails .....{to_email},{password}")
        send_mail(subject,message,from_email,[to_email],fail_silently=False)
        print(f"mail sent success")
    except Exception as e:
        print("Error in sending mail")
        print(e)


def send_log_mail(message):
    subject = "CSC cron job data log"
    from_email = getattr(settings, "NO_REPLY_MAIL", "no-reply@spoken-tutorial.org")
    to_email = "web-query@spoken-tutorial.org"
    try:
        send_mail(subject,message,from_email,to_email,fail_silently=False)
        print(f"sending mail .....{to_email},{message}")
    except:
        print("Unable to send csc update mail to web-team")

def getFirstName(name):
    formatted = name.split()
    if formatted:
        return formatted[0]
    return ''

def getLastName(name):
    formatted = name.split(maxsplit=1)
    if len(formatted)>1:
        return formatted[1]
    return ''

def add_vle(item,csc):
    print(f"add_vle".ljust(40,'-'))
    try:
        user = User.objects.get(Q(email=item.get('email')) | Q(username=item.get('email')))
        print(f"user for vle {item.get('email')} exists")
    except User.DoesNotExist:
        print(f"user for vle {item.get('email')} does not exists")
        user = User.objects.create(
                            username=item['email'],first_name=getFirstName(item['name']),last_name=getLastName(item['name']),
                            email=item['email'],is_staff=0,is_active=1
                        )
        print(f"user for vle {item.get('email')} created")
    # IMPORTANT ToDo: REMOVE static pwd
    password = ''.join([ random.choice(string.ascii_letters+string.digits) for x in range(8)])
    
    enc_password = make_password(password)
    user.password = enc_password
    user.save()
    send_password_mail(user,password)
    try:
        print(f"creating vle ....{user}")
        vle = VLE.objects.create(
            csc=csc,user=user,phone=item['phone'],status=1
        )
        vle_group = Group.objects.get(name='VLE')
        vle_group.user_set.add(user)
        print(f"created vle .... {user}")
    except IntegrityError as e: 
        print(f"vle already exists ....")
        vle = VLE.objects.get(Q(csc=csc) and Q(user=user))
    tdate = item.get('transcdate').split()[0]
    
    tdate = datetime.strptime(tdate,'%Y-%m-%d')
    print(f"tdate ************************ {tdate}")
    try:
        tenure_end_date = get_tenure_end_date(tdate)
        print(f"**tenure_end_date : {tenure_end_date}")
        transaction = Transaction.objects.create(vle=vle,csc=csc,transcdate=tdate,tenure=None,tenure_end_date=tenure_end_date)
    except Exception as e: 
        print(e)

def add_transaction(vle,csc,transcdate):
    print('checking Transaction Dates ....................')
    tdate = transcdate.split()[0]
    transaction = Transaction.objects.filter(vle=vle,csc=csc,transcdate=tdate)
    if not transaction:
        transaction = Transaction.objects.create(vle=vle,csc=csc,transcdate=tdate,tenure=None,tenure_end_date=None)
        print('Added Transaction Dates ....................')

    