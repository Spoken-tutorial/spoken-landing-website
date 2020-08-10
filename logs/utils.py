
from analytics_system import MONGO_CLIENT


db = MONGO_CLIENT.logs
tutorial_progress_logs = db.tutorial_progress_logs

def update_tutorial_progress(data):

    field = 'fosses.' + str(data['foss_id']) + '.' + str(data['language_id']) + '.' + str(data['tutorial_id'])

    curr_time_field = field + '.curr_time'
    time_field = field + '.visits.' + str (data['language_visit_count']) + '.minute-' + str(data['curr_time'])
    completed_field = field + '.completed'

    try:
        # mark as complete if current timestamp >= 80% of total length of tutorial
        if data['allow_completion_change'] == 'true' and data['curr_time'] >= 0.8 * data['total_time']:

            tutorial_progress_logs.find_one_and_update(
                { "username" : data['username'] }, 
                { "$set" : { curr_time_field: data['curr_time'], completed_field: True } },
                upsert=True
            )

            tutorial_progress_logs.find_one_and_update(
                { "username" : data['username'] },
                { "$push" : { time_field : data["datetime"] } },
                upsert=True
            )

            return

        # if curr_time is not yet 80% of total or completion change is not allowed.

        tutorial_progress_logs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$set" : { curr_time_field: data['curr_time'] } },
            upsert=True
        )
            
        tutorial_progress_logs.find_one_and_update(
            { "username" : data['username'] }, 
            { "$push" : { time_field : data["datetime"] } },
            upsert=True
        )
        
        
    except Exception as e:
        with open("logs/tutorial_errors_log.txt", "a") as f:
            f.write(str(e) + "\n")