# Generated by Django 3.0.3 on 2022-07-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csc', '0014_auto_20220719_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='invigilator',
            name='vle',
            field=models.ManyToManyField(to='csc.VLE'),
        ),
    ]