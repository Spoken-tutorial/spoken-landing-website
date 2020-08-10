from django.core.cache import cache
import requests

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