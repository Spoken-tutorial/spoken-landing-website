# Generated by Django 3.0.3 on 2022-05-26 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CSC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csc_id', models.CharField(max_length=50)),
                ('institute', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('block', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('pincode', models.CharField(max_length=6)),
                ('plan', models.CharField(choices=[('College Level Subscription', 'College Level Subscription'), ('School Level Subscription', 'School Level Subscription')], max_length=100)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='VLE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True)),
                ('csc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.CSC')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transcdate', models.DateField()),
                ('tenure', models.CharField(choices=[('quarterly', 'quarterly'), ('biannually', 'biannually'), ('annually', 'annually')], max_length=10)),
                ('tenure_end_date', models.DateField()),
                ('csc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.CSC')),
                ('vle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.VLE')),
            ],
        ),
    ]
