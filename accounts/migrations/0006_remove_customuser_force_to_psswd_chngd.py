# Generated by Django 4.0 on 2022-01-10 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_force_to_psswd_chngd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='force_to_psswd_chngd',
        ),
    ]
