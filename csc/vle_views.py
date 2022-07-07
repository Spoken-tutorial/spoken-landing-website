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


def vle_dashboard(request):
    context = {}
    foss_form = FossForm()
    context['form']=foss_form
    return render(request, 'csc/vle.html',context)


# @csrf_exempt
# def ajax_get_spoken_foss(request):
#     """Ajax: Get foss according to programme type"""

#     if request.method == 'POST':
#         programme_type = request.POST.get('programme_type')
#         if programme_type == 'dca':
#             foss = SpokenFoss.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
#         else:
#             foss = SpokenFoss.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')
#         html = '<option value=None> --------- </option>'
#         if foss:
#             for fs in foss:
#                 html += '<option value={0}>{1}</option>'.format(fs.id,
#                         fs.foss)
#     return HttpResponse(json.dumps(html),
#                         content_type='application/json')



class GetFossOptionView(JSONResponseMixin, View):
  def dispatch(self, *args, **kwargs):
    return super(GetFossOptionView, self).dispatch(*args, **kwargs)

  def post(self, request, *args, **kwargs):
    programme_type = self.request.POST.get('programme_type')
    context = {}

    foss_option = "<option value=''>---------</option>"


    if programme_type == 'dca':
        fosses = SpokenFoss.objects.filter(csc_dca_programme=True, available_for_jio=True).order_by('foss')
    else:
        fosses = SpokenFoss.objects.filter(csc_dca_programme=False, available_for_jio=True).order_by('foss')

    for foss in fosses:
      foss_option += "<option value=" + str(foss.id) + ">" + str(foss.foss) + "</option>"
    context = {
      'spoken_foss_option' : foss_option,
    }
    return self.render_to_json_response(context)


