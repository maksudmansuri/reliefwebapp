# Generated by Django 3.2.5 on 2021-12-08 04:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0017_orderbooking_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooking',
            name='is_report_uploaded',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='orderbooking',
            name='report_upload_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 1, 0, 0), null=True),
        ),
        migrations.AlterField(
            model_name='orderbooking',
            name='reject_within_5',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 1, 0, 0), null=True),
        ),
    ]
