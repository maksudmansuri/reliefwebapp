# Generated by Django 3.2.5 on 2021-09-23 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_picturesformedicine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picturesformedicine',
            name='report',
        ),
    ]