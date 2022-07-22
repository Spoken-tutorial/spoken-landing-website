from django.db import models
from csc.models import FossCategory

# Create your models here.
class SpokenUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        #app_label = 'spoken'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=10, default='en')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        managed = False
        db_table = 'creation_language'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Level(models.Model):
    level = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    class Meta(object):
        managed = False
        db_table = 'creation_level'

    def __str__(self):
        return self.level

class TutorialDetail(models.Model):
    foss = models.ForeignKey(FossCategory, on_delete=models.PROTECT )
    tutorial = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.PROTECT )
    order = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        managed = False
        db_table = 'creation_tutorialdetail'
        unique_together = (('foss', 'tutorial', 'level'),)

    def __str__(self):
        return self.tutorial


class TutorialCommonContent(models.Model):
    tutorial_detail = models.OneToOneField(
        TutorialDetail, related_name='tutorial_detail',on_delete=models.PROTECT)
    slide = models.CharField(max_length=255)
    slide_status = models.PositiveSmallIntegerField(default=0)

    code = models.CharField(max_length=255)
    code_status = models.PositiveSmallIntegerField(default=0)

    assignment = models.CharField(max_length=255)
    assignment_status = models.PositiveSmallIntegerField(default=0)

    prerequisite = models.ForeignKey(
        TutorialDetail, related_name='prerequisite', blank=True, null=True, on_delete=models.PROTECT )
    prerequisite_status = models.PositiveSmallIntegerField(default=0)

    additional_material = models.CharField(
        max_length=255, blank=True, null=True)
    additional_material_status = models.PositiveSmallIntegerField(default=0)

    keyword = models.TextField()
    keyword_status = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        managed = False
        db_table = 'creation_tutorialcommoncontent'

    def keyword_as_list(self):
        return self.keyword.split(',')


class TutorialResource(models.Model):
    tutorial_detail = models.ForeignKey(TutorialDetail, on_delete=models.PROTECT )
    common_content = models.ForeignKey(TutorialCommonContent, on_delete=models.PROTECT )
    language = models.ForeignKey(Language, on_delete=models.PROTECT )

    outline = models.TextField()
    outline_status = models.PositiveSmallIntegerField(default=0)

    script = models.URLField(max_length=255)
    script_status = models.PositiveSmallIntegerField(default=0)
    timed_script = models.URLField(max_length=255)

    video = models.CharField(max_length=255)
    video_id = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    playlist_item_id = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    video_thumbnail_time = models.TimeField(default='00:00:00')
    video_status = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=0)
    version = models.PositiveSmallIntegerField(default=0)
    hit_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'creation_tutorialresource'
        unique_together = ('tutorial_detail', 'language',)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('watch_tutorial', args=[self.tutorial_detail.foss.foss, self.tutorial_detail.tutorial, self.language])

