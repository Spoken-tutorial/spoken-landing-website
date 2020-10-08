import requests
from requests.auth import HTTPBasicAuth
import os


def send_completion_data(data):
    requests.post(os.getenv("NASSCOM_XAPI_URL"), auth=HTTPBasicAuth(os.getenv("NASSCOM_XAPI_USERNAME"), os.getenv("NASSCOM_XAPI_PASSWORD")),data = data)


def get_payload(instance):
    data = {
            "actor": {
                "name": instance.user.first_name +" "+instance.user.last_name,
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
                    "en-US": instance.foss+"-"+instance.language
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