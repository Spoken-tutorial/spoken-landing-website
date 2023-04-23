from csc.models import VLE, Transaction
from datetime import date
from django.conf import settings
def is_vle_valid(request):
    is_valid_vle = False
    valid_days = 0
    alert_tag = 'danger'
    user = request.user
    vle = None
    expire_date = None
    if user.is_authenticated:
        vle = VLE.objects.filter(user=user).first()
        if vle:
            expire_date = Transaction.objects.filter(vle=vle).order_by('-tenure_end_date').values('tenure_end_date')[0]['tenure_end_date']
            current_date = date.today()
            if  current_date <= expire_date:
                is_valid_vle = True
                date_diff = expire_date - current_date 
                valid_days = date_diff.days 
                ALERT_DAYS = int(getattr(settings, 'ALERT_DAYS'))
                if valid_days > ALERT_DAYS:
                    alert_tag = 'info'
    renewal_info = 'Your account is restricted due to non-renewal of subscription.'
    return {'is_valid_vle':is_valid_vle,'alert_tag':alert_tag,'valid_days':valid_days,'tenure_end_date':expire_date,'renewal_info':renewal_info}
    