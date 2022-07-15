from django.urls import reverse
from re import template
from django.contrib.auth.views import LoginView
from django.views.generic import *
from django.shortcuts import render
from .utils import *
from csc.models import *
from spokenlogin.models import *
from django.http import JsonResponse
from .vle_forms import *

from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect



class JSONResponseMixin(object):
  """
  A mixin that can be used to render a JSON response.
  """
  def render_to_json_response(self, context, **response_kwargs):
    """
    Returns a JSON response, transforming 'context' to make the payload.
    """
    return JsonResponse(
        self.get_data(context),
        **response_kwargs
    )

  def get_data(self, context):
    """
    Returns an object that will be serialized as JSON by json.dumps().
    """
    # Note: This is *EXTREMELY* naive; in reality, you'll need
    # to do much more complex handling to ensure that arbitrary
    # objects -- such as Django model instances or querysets
    # -- can be serialized as JSON.
    return context

class CSCLogin(LoginView):
    template_name = 'csc/login.html'
    extra_context = {}

    def get_redirect_url(self):
        if is_user_vle(self.request.user): return reverse('csc:vle_dashboard')
        # ToDo if student ; redirect to student dashboard

@csrf_exempt
def vle_dashboard(request):
    context = {}
    user = request.user

    if request.method == 'POST':
        form = form = FossForm(request.POST)

        print(form)

        if form.is_valid():
            print('EEEEEEEEEEEEEEEEEE')
            # form_data = form.save(commit=False)            

            programme_type = form.cleaned_data['programme_type']
            print(programme_type, "!!!!!!!!!")

            spoken_foss = form.cleaned_data['spoken_foss']
            for sf in spoken_foss:
                print(sf.id,"$$$$$$$$$$$$$$$")
                #check if fossid already exist
                vfoss=Vle_csc_foss()

                vfoss.programme_type=programme_type
                vfoss.spoken_foss=sf.id
                try:
                    vfoss.save()
                    messages.success(request, form_data.spoken_foss+" has been added")
                except:
                    messages.success(request, "Records already present")
            
            return HttpResponseRedirect("/csc/vle/")

        context = {'form':form}
        return render(request, 'csc/vle.html', context)
    else:
        context.update(csrf(request))
        foss_form = FossForm()
        context['form']=foss_form
        return render(request, 'csc/vle.html',context)

@method_decorator(csrf_exempt, name='dispatch')
class GetFossOptionView(JSONResponseMixin, View):
  def dispatch(self, *args, **kwargs):
    return super(GetFossOptionView, self).dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
    programme_type = self.request.POST.get('programme_type')
    print(programme_type,"*****************")
    context = {}

    foss_option = "<option value=''>---------</option>"


    if programme_type == 'dca':
        fosses = SpokenFoss.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
    else:
        fosses = SpokenFoss.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')

    for foss in fosses:
      foss_option += "<option value=" + str(foss.id) + ">" + str(foss.foss) + "</option>"

    print(foss_option)
    context = {
      'spoken_foss_option' : foss_option,
    }
    return self.render_to_json_response(context)


