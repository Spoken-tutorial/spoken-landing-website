# Generated by Django 2.2.7 on 2020-03-23 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spoken', '0005_auto_20200305_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('order', models.IntegerField()),
                ('link', models.CharField(max_length=300)),
            ],
        ),
    ]
