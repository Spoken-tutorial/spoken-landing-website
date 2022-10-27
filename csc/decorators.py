from email import message
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .utils import is_user_vle,is_user_student,is_csc_team_role

# decorator 
def is_vle(view_func):
    def wrapper(request,*args,**kwargs):
        # ToDo : Role for VLE in group
        if is_user_vle(request.user):
            return view_func(request,*args,**kwargs)
        else:
            messages.add_message(request,messages.INFO,'Access denied')
            raise PermissionDenied()
    return wrapper

def is_student(view_func):
    def wrapper(request,*args,**kwargs):
        # ToDo : Role for STUDENT in group
        if is_user_student(request.user):
            return view_func(request,*args,**kwargs)
        else:
            messages.add_message(request,messages.INFO,'Access denied')
            raise PermissionDenied()
    return wrapper

def is_csc_team(view_func):
    def wrapper(request,*args,**kwargs):
        # ToDo : Role for VLE in group
        if is_csc_team_role(request.user):
            return view_func(request,*args,**kwargs)
        else:
            messages.add_message(request,messages.INFO,'Access denied')
            raise PermissionDenied()
    return wrapper