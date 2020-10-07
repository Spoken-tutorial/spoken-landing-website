from .models import CourseProgress
from spoken.utils import get_tutorials

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
        if instance.status:
            print("You have completd the course", instance.foss, instance.language)