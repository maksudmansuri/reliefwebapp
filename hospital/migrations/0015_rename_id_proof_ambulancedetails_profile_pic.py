# Generated by Django 3.2.5 on 2021-11-23 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0014_ambulancedetails_id_proof'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ambulancedetails',
            old_name='ID_proof',
            new_name='profile_pic',
        ),
    ]
