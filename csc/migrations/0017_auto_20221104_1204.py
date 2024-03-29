# Generated by Django 3.0.3 on 2022-11-04 06:34

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('csc', '0016_auto_20220930_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='test_name',
        ),
        migrations.AddField(
            model_name='invigilator',
            name='password_mail_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='mdl_mail_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='test',
            name='invigilator',
            field=models.ManyToManyField(blank=True, null=True, to='csc.Invigilator'),
        ),
        migrations.AddField(
            model_name='test',
            name='participant_count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='test',
            name='status',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invigilator',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='invigilator',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invi', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_registration',
            field=models.DateField(default=datetime.date(2022, 11, 4)),
        ),
        migrations.AlterField(
            model_name='test',
            name='publish',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='test',
            name='vle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='csc.VLE'),
        ),
        migrations.CreateModel(
            name='CSCFossMdlCourses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mdlcourse_id', models.PositiveIntegerField()),
                ('mdlquiz_id', models.PositiveIntegerField()),
                ('foss', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cscfoss', to='csc.FossCategory')),
                ('testfoss', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='testfoss', to='csc.FossCategory')),
            ],
        ),
        migrations.RemoveField(
            model_name='invigilator',
            name='added_by',
        ),
        migrations.CreateModel(
            name='CSCTestAtttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mdluser_id', models.PositiveIntegerField()),
                ('mdlcourse_id', models.PositiveIntegerField(default=0)),
                ('mdlquiz_id', models.PositiveIntegerField(default=0)),
                ('mdlattempt_id', models.PositiveIntegerField(default=0)),
                ('status', models.PositiveSmallIntegerField(default=0)),
                ('mdlgrade', models.DecimalField(decimal_places=5, default=0.0, max_digits=12)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='csc.Student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='csc.Test')),
            ],
            options={
                'verbose_name': 'Test Attendance',
                'unique_together': {('test', 'mdluser_id')},
            },
        ),
    ]
