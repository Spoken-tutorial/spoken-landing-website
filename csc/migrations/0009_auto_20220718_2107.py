# Generated by Django 3.0.3 on 2022-07-18 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csc', '0008_remove_fosscategory_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vle_csc_foss',
            name='spoken_foss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc.FossCategory'),
        ),
    ]