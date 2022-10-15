from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from csc.api.utility import send_pwd_mail

# Create your views here.
def password(request):
    print(request)
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.get(username=email)
        send_pwd_mail(user)
        return redirect('/')
    return render(request, 'registration/password.html')