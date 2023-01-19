# Generated by Django 3.0.3 on 2023-01-16 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('csc', '0022_auto_20230116_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_type', models.CharField(choices=[('ind', 'Individual Foss Course')], max_length=50)),
                ('background', models.FileField(upload_to='backgrounds')),
                ('parameters', models.TextField()),
                ('text_template', models.FileField(upload_to='templates')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=25)),
                ('test_attendance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.CSCTestAtttendance')),
            ],
        ),
    ]
