from django.db import models

# Create your models here.
class State(models.Model):
  code = models.CharField(max_length=3)
  name = models.CharField(max_length=50)
  slug = models.CharField(max_length = 100)
  latitude = models.DecimalField(
    null=True,
    max_digits=10,
    decimal_places=4,
    blank=True
  )
  longtitude = models.DecimalField(
    null=True,
    max_digits=10,
    decimal_places=4,
    blank=True
  )
  img_map_area = models.TextField()
  has_map = models.BooleanField(default=1)
  created = models.DateTimeField(auto_now_add = True, null=True)
  updated = models.DateTimeField(auto_now = True, null=True)

  def __str__(self):
    return self.name

  class Meta(object):
    unique_together = (("code","name"),)

class District(models.Model):
  state = models.ForeignKey(State, on_delete=models.PROTECT )
  code = models.CharField(max_length=3)
  name = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add = True, null=True)
  updated = models.DateTimeField(auto_now = True, null=True)

  def __str__(self):
    return self.name

  class Meta(object):
    unique_together = (("state", "code","name"),)

class City(models.Model):
  state = models.ForeignKey(State, on_delete=models.PROTECT )
  name = models.CharField(max_length=200)
  created = models.DateTimeField(auto_now_add = True, null=True)
  updated = models.DateTimeField(auto_now = True, null=True)

  def __str__(self):
    return self.name

  class Meta(object):
    unique_together = (("name","state"),)