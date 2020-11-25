from django.core.management.base import BaseCommand
from django.db import transaction as tx
from logs.models import CourseProgress
from logs.utils import send_completion_data, get_payload
from django.conf import settings

class Command(BaseCommand):

    @tx.atomic
    def handle(self, *args, **options):
        print("Sending course completion details to partner api...")
        count = 0
        courses = CourseProgress.objects.filter(status=True, completion_status_sent=False)
        for cr in courses:
            if cr.foss in settings.NASSCOM_COURSES and cr.language == "English":
                data = get_payload(cr)
                r = send_completion_data(data)
                if r:
                    if r.status_code == 200:
                        cr.completion_status_sent = True
                        cr.save()
                        count+=1
        print("Total course completion details sent to partner = ", count)
