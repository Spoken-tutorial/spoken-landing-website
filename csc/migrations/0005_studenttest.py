# Generated by Django 3.0.3 on 2022-07-27 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csc', '0004_auto_20220726_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.Student')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.Test')),
            ],
        ),
    ]
