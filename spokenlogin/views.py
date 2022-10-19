from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
            return redirect('/accounts/login')
        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'User Does Not Exist.')
            return redirect('/accounts/login')
    return render(request, 'registration/password.html')

@login_required(login_url='/accounts/login')
def change(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        new = request.POST['new']
        confirm = request.POST['confirm']
        if new != confirm:
            messages.add_message(request, messages.ERROR, 'Password did not match.')
        elif len(new) < 8:
            messages.add_message(request, messages.ERROR, 'Password should be 8 characters long.')
        elif not str(new).isalnum():
            messages.add_message(request, messages.ERROR, 'Password should contain only numbers and letters.')
        else:
            user.set_password(new)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
    return render(request, 'registration/change.html')