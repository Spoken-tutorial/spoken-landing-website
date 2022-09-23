from django.db import models
from django.contrib.auth.models import User
from csc.models import FossCategory
import datetime

# Create your models here.
class Level(models.Model):
    level = models.CharField(max_length=255)
    code = models.CharField(max_length=10)

    class Meta(object):
        verbose_name = 'Tutorial Level'

    def __str__(self):
        return self.level

class FossSuperCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'FOSS Category'
        verbose_name_plural = 'FOSS Categories'
        ordering = ('name',)
        managed = False
        db_table = 'creation_fosssupercategory'

    def __str__(self):
        return self.name

class FossCategory(models.Model):
    foss = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    status = models.BooleanField(max_length=2)
    is_learners_allowed = models.BooleanField(max_length=2,default=0 )
    is_translation_allowed = models.BooleanField(max_length=2, default=0)
    # user = models.ForeignKey(User, on_delete=models.PROTECT )
    category = models.ManyToManyField(FossSuperCategory)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    show_on_homepage = models.PositiveSmallIntegerField(default=0, help_text ='0:Series, 1:Display on home page, 2:Archived')
    available_for_nasscom = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for nasscom' )
    available_for_jio = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for jio and spoken-tutorial.in' )
    csc_dca_programme = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for csc-dca programme' )
    class Meta(object):
        verbose_name = 'FOSS'
        verbose_name_plural = 'FOSSes'
        ordering = ('foss', )
        managed = False
        db_table = 'creation_fosscategory'

    def __str__(self):
        return self.foss

class TutorialDetail(models.Model):
    foss = models.ForeignKey(FossCategory, on_delete=models.PROTECT )
    tutorial = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.PROTECT )
    order = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'Tutorial Detail'
        unique_together = (('foss', 'tutorial', 'level'),)
        managed = False
        db_table = 'creation_tutorialdetail'

    def __str__(self):
        return self.tutorial
class TutorialCommonContent(models.Model):
    tutorial_detail = models.OneToOneField(
        TutorialDetail, related_name='tutorial_detail',on_delete=models.PROTECT)
    slide = models.CharField(max_length=255)
    slide_user = models.ForeignKey(User, related_name='slides', on_delete=models.PROTECT )
    slide_status = models.PositiveSmallIntegerField(default=0)

    code = models.CharField(max_length=255)
    code_user = models.ForeignKey(User, related_name='codes', on_delete=models.PROTECT )
    code_status = models.PositiveSmallIntegerField(default=0)

    assignment = models.CharField(max_length=255)
    assignment_user = models.ForeignKey(User, related_name='assignments', on_delete=models.PROTECT )
    assignment_status = models.PositiveSmallIntegerField(default=0)

    prerequisite = models.ForeignKey(
        TutorialDetail, related_name='prerequisite', blank=True, null=True, on_delete=models.PROTECT )
    prerequisite_user = models.ForeignKey(User, related_name='prerequisite', on_delete=models.PROTECT )
    prerequisite_status = models.PositiveSmallIntegerField(default=0)

    additional_material = models.CharField(
        max_length=255, blank=True, null=True)
    additional_material_user = models.ForeignKey(
        User, related_name='additional_material', null=True, default=None, on_delete=models.PROTECT )
    additional_material_status = models.PositiveSmallIntegerField(default=0)

    keyword = models.TextField()
    keyword_user = models.ForeignKey(User, related_name='keywords', on_delete=models.PROTECT )
    keyword_status = models.PositiveSmallIntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        verbose_name = 'Tutorial Common Content'

    def keyword_as_list(self):
        return self.keyword.split(',')

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT )
    code = models.CharField(max_length=10, default='en')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('name',)
        managed = False
        db_table = 'creation_language'

    def __str__(self):
        return self.name

class TutorialResource(models.Model):
    tutorial_detail = models.ForeignKey(TutorialDetail, on_delete=models.PROTECT )
    common_content = models.ForeignKey(TutorialCommonContent, on_delete=models.PROTECT )
    language = models.ForeignKey(Language, on_delete=models.PROTECT )

    outline = models.TextField()
    outline_user = models.ForeignKey(User, related_name='outlines', on_delete=models.PROTECT )
    outline_status = models.PositiveSmallIntegerField(default=0)

    script = models.URLField(max_length=255)
    script_user = models.ForeignKey(User, related_name='scripts', on_delete=models.PROTECT )
    script_status = models.PositiveSmallIntegerField(default=0)
    timed_script = models.URLField(max_length=255)

    video = models.CharField(max_length=255)
    video_id = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    playlist_item_id = models.CharField(
        max_length=255, null=True, blank=True, default=None)
    video_thumbnail_time = models.TimeField(default='00:00:00')
    video_user = models.ForeignKey(User, related_name='videos', on_delete=models.PROTECT )
    video_status = models.PositiveSmallIntegerField(default=0)
    status = models.PositiveSmallIntegerField(default=0)
    version = models.PositiveSmallIntegerField(default=0)
    hit_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish_at = models.DateTimeField(null=True)
    # the last submission date for the tutorial
    submissiondate = models.DateTimeField(default=datetime.datetime(2000, 1, 2, 12, 00))
    # 0 - Not Assigned to anyone , 1 - Assigned & work in progress , 2 - Completed (= published / PR )
    assignment_status = models.PositiveSmallIntegerField(default=0)
    # 0 - Not Extended , 1 - Extended , 2 - Tutorial Terminated from user
    extension_status = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('tutorial_detail', 'language',)
        managed = False
        db_table = 'creation_tutorialresource'
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('watch_tutorial', args=[self.tutorial_detail.foss.foss, self.tutorial_detail.tutorial, self.language])




# Forums models

class Question(models.Model):
  uid  = models.IntegerField()
  category = models.CharField(max_length=200)
  tutorial = models.CharField(max_length=200)
  minute_range = models.CharField(max_length=10)
  second_range = models.CharField(max_length=10)
  title = models.CharField(max_length=200)
  body = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  views = models.IntegerField(default=1)
  status = models.IntegerField(default=1)
  # votes = models.IntegerField(default=0)

  def get_slugified_title(self):
    return self.title.replace(' ', '-')

  def user(self):
    user = User.objects.get(id=self.uid)
    return user.username

  class Meta(object):
    db_table = 'website_question'
    get_latest_by = "date_created"

class Answer(models.Model):
  uid  = models.IntegerField()
  question = models.ForeignKey(Question, on_delete=models.PROTECT )
  body = models.TextField()
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  # votes = models.IntegerField(default=0)

  def user(self):
    user = User.objects.get(id=self.uid)
    return user.username

  class Meta(object):
    db_table = 'website_answer'