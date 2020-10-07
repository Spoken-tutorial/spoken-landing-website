from django.apps import AppConfig
from django.db.models.signals import post_save

class LogsConfig(AppConfig):
    name = 'logs'

    def ready(self):
        from .models import TutorialProgress, CourseProgress
        from .signals import tutorial_progress_signal, course_completion_signal
        post_save.connect(tutorial_progress_signal, sender=TutorialProgress, dispatch_uid='trigger_tutorial_progress')
        post_save.connect(course_completion_signal, sender=CourseProgress, dispatch_uid='trigger_course_completion')
