from django.conf import settings
from django.urls import reverse
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponseServerError)
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from .views import prepare_django_request, init_saml_auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class SSO:

    def __init__(self, get_response):
        self.LOG_CLASS = "SSO_MIDDLEWARE"
        self.get_response = get_response

    def __call__(self, request):
        req = prepare_django_request(request)
        auth = init_saml_auth(req)
        errors = []
        error_reason = None
        not_auth_warn = False
        success_slo = False
        attributes = False
        paint_logout = False

        if 'sso' in req['get_data']:
            return HttpResponseRedirect(auth.login())
            # If AuthNRequest ID need to be stored in order to later validate it, do instead
            # sso_built_url = auth.login()
            # request.session['AuthNRequestID'] = auth.get_last_request_id()
            # return HttpResponseRedirect(sso_built_url)
        elif 'sso2' in req['get_data']:
            req['get_data'].pop('sso2')
            return_to = OneLogin_Saml2_Utils.get_self_url(req) + request.META['PATH_INFO']+'?'+req['get_data'].urlencode()
            return HttpResponseRedirect(auth.login(return_to))
        elif 'acs' in req['get_data']:
            request_id = None
            if 'AuthNRequestID' in request.session:
                request_id = request.session['AuthNRequestID']

            auth.process_response(request_id=request_id)
            errors = auth.get_errors()
            not_auth_warn = not auth.is_authenticated()

            if not errors:
                if 'AuthNRequestID' in request.session:
                    del request.session['AuthNRequestID']
                request.session['samlUserdata'] = auth.get_attributes()
                request.session['samlNameId'] = auth.get_nameid()
                request.session['samlNameIdFormat'] = auth.get_nameid_format()
                request.session['samlNameIdNameQualifier'] = auth.get_nameid_nq()
                request.session['samlNameIdSPNameQualifier'] = auth.get_nameid_spnq()
                request.session['samlSessionIndex'] = auth.get_session_index()

                user = authenticate(request, auth=auth)
                if user is not None:
                    login(request, user)                 
                if 'RelayState' in req['post_data'] and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
                    if not req['post_data']['RelayState']:
                        req['post_data']['RelayState'] = request.build_absolute_uri('/')
                    return HttpResponseRedirect(auth.redirect_to(req['post_data']['RelayState']))
            elif auth.get_settings().is_debug_active():
                    error_reason = auth.get_last_error_reason()
        elif 'sls' in req['get_data']:
            request_id = None
            if 'LogoutRequestID' in request.session:
                request_id = request.session['LogoutRequestID']
            dscb = lambda: request.session.flush()
            url = auth.process_slo(request_id=request_id, delete_session_cb=dscb)
            errors = auth.get_errors()
            if len(errors) == 0:
                if url is not None:
                    return HttpResponseRedirect(url)
                else:
                    success_slo = True
            elif auth.get_settings().is_debug_active():
                error_reason = auth.get_last_error_reason()
        return self.get_response(request)






  