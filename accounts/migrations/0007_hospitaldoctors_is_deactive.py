# Generated by Django 4.0 on 2022-01-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_customuser_force_to_psswd_chngd'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaldoctors',
            name='is_deactive',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]