# Generated by Django 3.0.3 on 2022-07-18 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csc', '0006_auto_20220713_1724'),
    ]

    operations = [
        migrations.CreateModel(
            name='FossSuperCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'FOSS Category',
                'verbose_name_plural': 'FOSS Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('gender', models.CharField(blank=True, max_length=10)),
                ('dob', models.DateField(blank=True)),
                ('phone', models.CharField(blank=True, max_length=32)),
                ('edu_qualification', models.CharField(blank=True, max_length=255)),
                ('pincode', models.CharField(blank=True, max_length=6)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('date_of_registration', models.DateField()),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.City')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.District')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.State')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vle_id', models.ManyToManyField(to='csc.VLE')),
            ],
        ),
        migrations.AddField(
            model_name='vle_csc_foss',
            name='vle',
            field=models.ForeignKey(default=11, on_delete=django.db.models.deletion.CASCADE, to='csc.VLE'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FossCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foss', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('status', models.BooleanField(max_length=2)),
                ('is_learners_allowed', models.BooleanField(default=0, max_length=2)),
                ('is_translation_allowed', models.BooleanField(default=0, max_length=2)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('show_on_homepage', models.PositiveSmallIntegerField(default=0, help_text='0:Series, 1:Display on home page, 2:Archived')),
                ('available_for_nasscom', models.BooleanField(default=True, help_text='If unchecked, this foss will not be available for nasscom')),
                ('available_for_jio', models.BooleanField(default=True, help_text='If unchecked, this foss will not be available for jio and spoken-tutorial.in')),
                ('csc_dca_programme', models.BooleanField(default=True, help_text='If unchecked, this foss will not be available for csc-dca programme')),
                ('category', models.ManyToManyField(to='csc.FossSuperCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'FOSS',
                'verbose_name_plural': 'FOSSes',
                'ordering': ('foss',),
            },
        ),
        migrations.CreateModel(
            name='Student_Foss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csc_foss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.Vle_csc_foss')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.Student')),
            ],
            options={
                'unique_together': {('student', 'csc_foss')},
            },
        ),
    ]