# Generated by Django 3.2.5 on 2021-12-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_auto_20211208_0930'),
    ]

    operations = [
        migrations.AddField(
            model_name='newlabtest',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]