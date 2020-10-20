from django.core.cache import cache
import requests
from logs.models import TutorialProgress,CourseProgress

def get_spokentutorials():
    spokentutorials = cache.get('spokentutorials')
    if spokentutorials:
        return spokentutorials
    else:
        spokentutorials = requests.get('https://spoken-tutorial.org/api/spoken_tutorial_videos/')
        spokentutorials = spokentutorials.json()['spokentutorials']
        cache.set('spokentutorials', spokentutorials)
        return spokentutorials

def get_foss_lists():
    spokentutorials = get_spokentutorials()
    return [foss['category'] for foss in spokentutorials]

def get_foss_languages(foss):
    spokentutorials = get_spokentutorials()
    for f in spokentutorials:
        if f['category'] == foss:
            return [ i['language'] for i in f['lists']]

def get_tutorials(foss, lang):
    spokentutorials = get_spokentutorials()
    for f in spokentutorials:
        if f['category'] == foss:
            for i in f['lists']:
                if i['language'] == lang:
                    return i['videos']

def get_tutorial_detail(foss, lang, tutorial):
    tutorials = get_tutorials(foss, lang)
    for t in tutorials:
        if t['title'] == tutorial:
            return t

def get_all_foss_lang():
    foss = get_foss_lists()
    return [{'foss': f, 'languages': get_foss_languages(f)} for f in foss]

def get_tutorials_completion_status(foss, lang, user):
    tutorials = get_tutorials(foss, lang)
    ts=[]
    for t in tutorials:
        try:
            tp=TutorialProgress.objects.get(
                user=user, 
                tutorial=t['title'],
                foss=foss,
                language=lang
                )
            tutorial_views = TutorialProgress.objects.filter(tutorial=t['title'],
                foss=foss,
                language=lang).count()
            t['status']=tp.status
            t['time_completed'] =tp.time_completed
            t['total_duration'] =tp.total_duration
            t['views'] = tutorial_views
        except:
            t['status'] =False
            t['time_completed'] =0
            t['total_duration'] =0
            t['views'] = 0
        ts.append(t)
    return ts

def get_course_progress(request):
    cp = []
    if request.user.is_authenticated:
        courseProgress = CourseProgress.objects.all().filter(user=request.user)
        for c in courseProgress:
            a = {}
            a["foss"] = c.foss
            a["progress"] = (c.tutorials_completed/c.total_tutorials) * 100
            cp.append(a)
    return cp



