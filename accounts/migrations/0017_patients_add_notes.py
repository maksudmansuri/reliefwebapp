# Generated by Django 3.2.5 on 2021-09-05 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20210822_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='add_notes',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
