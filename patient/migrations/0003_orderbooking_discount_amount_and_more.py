# Generated by Django 4.0.1 on 2022-01-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_orderbooking_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooking',
            name='discount_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='orderbooking',
            name='discount_rate',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
