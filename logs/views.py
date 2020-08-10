from django.shortcuts import render

# Create your views here.


@csrf_exempt
@require_POST
def save_tutorial_progress (request):
    """
    Function for handling the AJAX call of saving tutorial progress data. This AJAX
    call is made in watch_tutorial.html. Calls update_tutorial_progress in utils.py
    for the actual saving in MongoDB. Don't let users make their own post requests to this view. Remove CSRF exempt
    """

    data = {}
    data['username'] = request.POST.get("username")
    # data['foss'] = request.POST.get("foss")
    # data['foss_lang'] = request.POST.get("foss_lang")
    # data['tutorial'] = request.POST.get("tutorial")
    data['foss_id'] = request.POST.get("foss_id")
    data['tutorial_id'] = request.POST.get("tutorial_id")
    data['language_id'] = request.POST.get("language_id")
    data['curr_time'] = int (request.POST.get("curr_time"))
    data['total_time'] = int (request.POST.get("total_time"))

    # sometimes, on the first video play,
    # this duration is returned as 0 by video.js
    if (data['total_time'] == 0):
        data['total_time'] = math.inf

    data['language_visit_count'] = int (request.POST.get("language_visit_count"))
    data['datetime'] = datetime.datetime.fromtimestamp(int (request.POST.get("timestamp"))/1000)
    data['allow_completion_change'] = request.POST.get("allow_completion_change")

    update_tutorial_progress (data)  # synchronous call

    return HttpResponse(status=200)

@csrf_exempt
@require_POST
def change_completion (request):
    """
    Function for handling the AJAX call of changing tutorial completion data. This AJAX
    call is made in watch_tutorial.html. Don't let users make their own post requests to this view. Remove CSRF exempt
    """

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    # store in MongoDB
    try:
        
        completed = False
        if request.POST.get("completed") == "true":
            completed = True

        # TODO: don't allow dots in the FOSS names and tutorial names
        completed_field = 'fosses.' + str(request.POST.get('foss_id')) + '.' + str(request.POST.get('language_id')) + '.' + str(request.POST.get('tutorial_id')) + '.completed'
        tutorial_progress_logs.find_one_and_update(
                { "username" : request.POST.get('username') }, 
                { "$set" : { completed_field: completed } },
                upsert=True
        )

        return HttpResponse(status=200)

    except Exception as e:
        with open("change_completion_errors.txt", "a") as f:
            f.write(str(e) + '\n')
        
    return HttpResponse(status=500)



@csrf_exempt
@require_POST
def check_completion (request):
    """
    Function for handling the AJAX call of checking tutorial completion. This AJAX
    call is made in watch_tutorial.html. Don't let users make their own post requests to this view. Remove CSRF exempt
    """

    # configurations for pymongo
    db = MONGO_CLIENT.logs
    tutorial_progress_logs = db.tutorial_progress_logs

    try:

        res = tutorial_progress_logs.find_one(
            { "username" : request.POST.get('username') }
        )

        if res['fosses'][str(request.POST.get('foss_id'))][str(request.POST.get('language_id'))][str(request.POST.get('tutorial_id'))]['completed'] == True:
            return HttpResponse(status=200)

    except Exception:  # the 'completed' field is not yet created for that log.
        pass
    
    return HttpResponse(status=500)