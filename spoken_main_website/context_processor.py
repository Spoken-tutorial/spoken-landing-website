from django.conf import settings

def settings_val(request):
    context = {}
    context['google_tag'] = getattr(settings, "GOOGLE_TAG", "G-BRT8TPGCE1")
    return context