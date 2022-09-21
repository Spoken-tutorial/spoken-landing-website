# Generated by Django 3.0.3 on 2022-09-12 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csc', '0007_categorycourses_certifiatecategories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_foss',
            name='csc_foss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.FossCategory'),
        ),
        migrations.CreateModel(
            name='Student_certificate_course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('programme_starting_date', models.DateField(blank=True, null=True)),
                ('created', models.DateField(blank=True, null=True)),
                ('updated', models.DateField(auto_now=True, null=True)),
                ('cert_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.CertifiateCategories')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.Student')),
            ],
            options={
                'unique_together': {('student', 'cert_category')},
            },
        ),
    ]