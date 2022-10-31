from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from csc.api.utility import send_pwd_mail
from django.contrib import messages

# Create your views here.
def password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try: 
            user = User.objects.get(username=email)
            send_pwd_mail(user)
            messages.add_message(request, messages.SUCCESS, 'Password Mail Sent Successfully.')
            return redirect('/')
        except User.DoesNotExist:
            messages.add_message(request, messages.WARNING, 'User DoesNotExist.')
            return redirect('/')
    return render(request, 'registration/password.html')

def change(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        new = request.POST['new']
        confirm = request.POST['confirm']
        if new == confirm:
            user.set_password(new)
            user.save()
        messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
        return redirect('/')
    return render(request, 'registration/change.html')
