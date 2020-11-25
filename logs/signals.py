from .models import CourseProgress
from spoken.utils import get_tutorials
from .utils import send_completion_data, get_payload
from django.conf import settings
from sso.models import NasscomUser

def tutorial_progress_signal(sender, instance, created, **kwargs):
    if created or not created:
        if instance.status:
            try:
                cp = CourseProgress.objects.get(user=instance.user, foss=instance.foss, language=instance.language)
                cp.tutorials_completed += 1
                if cp.tutorials_completed == cp.total_tutorials:
                    cp.status = True
                cp.save()
            except CourseProgress.DoesNotExist:
                t = get_tutorials(instance.foss, instance.language)
                status = True if len(t) == 1 else False
                CourseProgress.objects.create(user=instance.user, foss=instance.foss, language=instance.language, total_tutorials = len(t), tutorials_completed=1, status = status)

def course_completion_signal(sender, instance, created, **kwargs):
    if created or not created:
        try:
            NasscomUser.objects.get(user=instance.user)
            if instance.foss in settings.NASSCOM_COURSES and instance.language == "English":
                if not instance.completion_status_sent:
                    if instance.status:
                        data = get_payload(instance)
                        r = send_completion_data(data)
                        if r:
                            if r.status_code == 200:
                                instance.completion_status_sent = True
                                instance.save()
        except NasscomUser.DoesNotExist:
            pass
            