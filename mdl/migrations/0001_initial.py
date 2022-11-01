# Generated by Django 3.0.3 on 2022-10-31 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MdlQuizAttempts',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('quiz', models.BigIntegerField()),
                ('userid', models.BigIntegerField()),
                ('attempt', models.IntegerField(unique=True)),
                ('uniqueid', models.BigIntegerField(unique=True)),
                ('layout', models.TextField()),
                ('currentpage', models.BigIntegerField()),
                ('preview', models.IntegerField()),
                ('state', models.CharField(max_length=48)),
                ('timestart', models.BigIntegerField()),
                ('timefinish', models.BigIntegerField()),
                ('timemodified', models.BigIntegerField()),
                ('timemodifiedoffline', models.BigIntegerField()),
                ('timecheckstate', models.BigIntegerField(blank=True, null=True)),
                ('sumgrades', models.DecimalField(blank=True, decimal_places=5, max_digits=12, null=True)),
            ],
            options={
                'db_table': 'mdl_quiz_attempts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MdlQuizGrades',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('quiz', models.BigIntegerField()),
                ('userid', models.BigIntegerField()),
                ('grade', models.DecimalField(decimal_places=5, max_digits=12)),
                ('timemodified', models.BigIntegerField()),
            ],
            options={
                'db_table': 'mdl_quiz_grades',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MdlUser',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=96)),
                ('idnumber', models.CharField(max_length=765)),
                ('firstname', models.CharField(max_length=300)),
                ('lastname', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'mdl_user',
                'managed': False,
            },
        ),
    ]
