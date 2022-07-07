from django.urls import reverse
from re import template
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from .utils import *

class CSCLogin(LoginView):
    template_name = 'csc/login.html'
    extra_context = {}

    def get_redirect_url(self):
        if is_user_vle(self.request.user): return reverse('csc:vle_dashboard')
        # ToDo if student ; redirect to student dashboard


def vle_dashboard(request):
    context = {}
    return render(request, 'csc/vle.html',context)

