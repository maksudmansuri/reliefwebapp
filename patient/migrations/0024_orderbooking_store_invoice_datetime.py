# Generated by Django 3.2.5 on 2021-12-08 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0023_rename_is_invoice_uploaded_orderbooking_store_invoice_uploaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooking',
            name='store_invoice_datetime',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 1, 1, 0, 0), null=True),
        ),
    ]