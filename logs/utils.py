import requests
from requests.auth import HTTPBasicAuth
import os
import json

def send_completion_data(data):
    try:
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        return requests.post(os.getenv("NASSCOM_XAPI_URL"), headers=headers, auth=HTTPBasicAuth(os.getenv("NASSCOM_XAPI_USERNAME"), os.getenv("NASSCOM_XAPI_PASSWORD")), data=json.dumps(data))
    except requests.ConnectionError:
        return False


def get_payload(instance):
    data = {
            "actor": {
                "name": instance.user.first_name +" "+instance.user.last_name if instance.user.first_name and instance.user.last_name else instance.user.email,
                "mbox": "mailto:"+instance.user.email
            },
            "verb": {
                "id": "http://activitystrea.ms/schema/1.0/complete",
                "display": {
                "en-US": "completed"
                }
            },  
            "object": {
                "id": "https://spoken-tutorial.in/spoken/tutorial-search/?search_foss={}&search_language={}".format(instance.foss, instance.language),
                "definition": {
                "name": {
                    "en-US": "Spoken-Tutorial-"+instance.foss.replace(' ', '-')+"-"+instance.language
                },
                "description": {
                    "en-US": instance.foss
                },
                "type": "http://adlnet.gov/expapi/activities/course"
                },
                "objectType": "Activity"
            }
    }
    return data