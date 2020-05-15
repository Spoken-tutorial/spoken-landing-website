# Generated by Django 3.0.5 on 2020-04-13 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('year', models.IntegerField(default=2020)),
                ('order', models.IntegerField(help_text='Award with lower order will appear first in the list')),
                ('link', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Blended_workshops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workshop_title', models.CharField(max_length=255)),
                ('workshop_start_date', models.DateField(blank=True, null=True)),
                ('workshop_end_date', models.DateField(blank=True, null=True)),
                ('workshop_content', models.TextField()),
                ('workshop_logo', models.FileField(blank=True, null=True, upload_to='logos/workshop_logos/')),
                ('know_more_link', models.CharField(max_length=300)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Blended Workshop',
                'verbose_name_plural': 'Blended Workshop',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='ContactMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Mails',
            },
        ),
        migrations.CreateModel(
            name='Internship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('internship_title', models.CharField(max_length=255)),
                ('internship_start_date', models.DateField(blank=True, null=True)),
                ('internship_end_date', models.DateField(blank=True, null=True)),
                ('internship_desc', models.TextField()),
                ('know_more_link', models.CharField(max_length=300)),
                ('updated', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaTestimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('spoken_tutorials', 'spoken tutorials'), ('school_system', 'school system'), ('forums', 'forums'), ('online_test', 'online test'), ('health_nutrition', 'health & nutrition')], default='spoken_tutorials', max_length=100)),
                ('user', models.CharField(max_length=255)),
                ('user_short_desc', models.CharField(default='', help_text='short description of user', max_length=255)),
                ('additional_details', models.CharField(default='Workshop', help_text='workshop, jobfair or other detail', max_length=255)),
                ('content', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('media', models.FileField(default='', upload_to='testimonials/')),
                ('show', models.BooleanField(default=1)),
            ],
            options={
                'verbose_name': 'Media Testimonial',
                'verbose_name_plural': 'Media Testimonials',
            },
        ),
        migrations.CreateModel(
            name='Nav',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nav_name', models.CharField(max_length=255)),
                ('nav_id', models.CharField(max_length=50)),
                ('data_section', models.CharField(max_length=50)),
                ('fa_icon', models.CharField(blank=True, max_length=50)),
                ('back_image', models.FileField(blank=True, null=True, upload_to='page_backgrounds/')),
                ('status', models.BooleanField(default=0)),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Navigation Tab',
                'verbose_name_plural': 'Navigation Tabs',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('product_url', models.CharField(max_length=300)),
                ('product_description', models.TextField()),
                ('logo', models.FileField(upload_to='logos/')),
                ('updated', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Testimonials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('user_short_description', models.CharField(blank=True, help_text='short description about user. Eg. college name, position', max_length=300, null=True)),
                ('actual_content', models.TextField()),
                ('category', models.CharField(choices=[('spoken_tutorials', 'spoken tutorials'), ('school_system', 'school system'), ('forums', 'forums'), ('online_test', 'online test'), ('health_nutrition', 'health & nutrition')], default='spoken_tutorials', max_length=100)),
                ('created', models.DateField(blank=True, null=True)),
                ('updated', models.DateField(auto_now=True, null=True)),
                ('show', models.BooleanField(default=1)),
            ],
            options={
                'verbose_name': 'Text Testimonial',
                'verbose_name_plural': 'Text Testimonials',
            },
        ),
        migrations.CreateModel(
            name='Jobfair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobfair_id', models.CharField(blank=True, max_length=50, null=True)),
                ('jobfair_title', models.CharField(max_length=255)),
                ('jobfair_start_date', models.DateField(blank=True, null=True)),
                ('jobfair_end_date', models.DateField(blank=True, null=True)),
                ('jobfair_desc', models.TextField()),
                ('know_more_link', models.CharField(max_length=300)),
                ('updated', models.DateField(auto_now=True)),
                ('num_students_registered', models.IntegerField(default=0)),
                ('num_students_placed', models.IntegerField(default=0)),
                ('eligibility_criteria', models.TextField(default='')),
                ('selection_process', models.TextField(default='')),
                ('num_student_appeared', models.IntegerField(default=0)),
                ('registration_start_date', models.DateField(blank=True, null=True)),
                ('registration_end_date', models.DateField(blank=True, null=True)),
                ('companies', models.ManyToManyField(to='spoken.Company')),
            ],
        ),
    ]