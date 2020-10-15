from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import *
from logs.models import TutorialProgress

class TutorialSearchAPI(APIView):
    """
    Search tutorial based on get url parameters. 
    Parameters: (search_foss, search_language)
    Example pattern: localhost:8000/spoken/api/tutorial-search/?search_foss=Advance+C&search_language=English
    """

    def get(self, request, format=None):
        context={}
        search_foss = request.query_params.get('search_foss', None)
        search_language = request.query_params.get('search_language', None)
        search_tutorial = request.query_params.get('search_tutorial', None)
        context["is_authenticated"] = request.user.is_authenticated
        if search_foss and search_language:
            context["foss"] = search_foss
            context["language"] = search_language
            context["foss_languages"] = get_foss_languages(search_foss)
            context["tutorials"] = get_tutorials_completion_status(search_foss, search_language, request.user) if request.user.is_authenticated else get_tutorials(search_foss, search_language)
            
            if search_tutorial:
                context["tutorial"] = get_tutorial_detail(search_foss, search_language, search_tutorial)
                if request.user.is_authenticated:
                    try:
                        context["is_authenticated"] = True
                        tp=TutorialProgress.objects.get(
                        user=request.user, 
                        tutorial=context["tutorial"]["title"],
                        foss=context["foss"],
                        language=context["language"]
                        )
                        context["total_duration"] = tp.total_duration
                        if tp.status:
                            time_completed=tp.total_duration
                        else:
                            time_completed=tp.time_completed
                        context["time_completed"] = time_completed
                        context["video_status"] = tp.status
                    except:
                        context["time_completed"] = 0
                        context["video_status"] = False
        context["foss_lang_list"] = get_all_foss_lang()
        return Response(context)
    