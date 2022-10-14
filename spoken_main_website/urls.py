"""spoken_main_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from spoken import views as spoken_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from spokenlogin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spoken/', include('spoken.urls')),
    path('api/jobfairs/', spoken_views.JobFairList.as_view()),
    path('sso/', include('sso.urls', namespace='sso')),
    path('logs/', include('logs.urls', namespace='logs')),
    url(r'^$', spoken_views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', spoken_views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='spokenlogin/login.html',redirect_authenticated_user=True), name='login_other'),
    # path('csc/', include('csc.vle_urls')),
    path('csc/student/', include('csc.student_urls', namespace='student')),
    path('csc/', include('csc.vle_urls', namespace='csc')),
    path('csc/api/v1/', include('csc.api.urls')),
    path('cms/api/v1/', include('cms.api.urls')),
    path('cdcontent/', include('cdcontent.urls')),
    
    path('accounts/', include('django.contrib.auth.urls')),

    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='password_change'),
    path('change_password_complete/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_complete.html'), name='password_complete'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='reset_password'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_form.html'), name='password_reset_confirm'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_sent.html'), name='reset_password_sent'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)