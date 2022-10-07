# Generated by Django 3.0.3 on 2022-10-06 05:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csc', '0016_auto_20220930_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='test_name',
        ),
        migrations.AddField(
            model_name='test',
            name='participant_count',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='test',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_registration',
            field=models.DateField(default=datetime.date(2022, 10, 6)),
        ),
        migrations.AlterField(
            model_name='test',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]
