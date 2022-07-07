from django.db import models

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

class SpFossSuperCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        db_table = 'creation_fosssupercategory'
        verbose_name = 'FOSS Category'
        verbose_name_plural = 'FOSS Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name

class SpokenFoss(models.Model):
    foss = models.CharField(unique=True, max_length=255)
    description = models.TextField()
    status = models.BooleanField(max_length=2)
    is_learners_allowed = models.BooleanField(max_length=2,default=0 )
    # is_translation_allowed = models.BooleanField(max_length=2, default=0)
    user = models.ForeignKey(SpokenUser, on_delete=models.PROTECT )
    category = models.ManyToManyField(SpFossSuperCategory)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    show_on_homepage = models.PositiveSmallIntegerField(default=0, help_text ='0:Series, 1:Display on home page, 2:Archived')
    available_for_nasscom = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for nasscom' )
    available_for_jio = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for jio, csc and spoken-tutorial.in' )
    csc_dca_programme = models.BooleanField(default=True, help_text ='If unchecked, this foss will not be available for csc-dca programme' )

    class Meta(object):
        db_table = 'creation_fosscategory'
        verbose_name = 'FOSS'
        verbose_name_plural = 'FOSSes'
        ordering = ('foss', )

    def __str__(self):
        return self.foss 