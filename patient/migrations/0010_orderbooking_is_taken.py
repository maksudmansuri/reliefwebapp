# Generated by Django 3.2.5 on 2021-12-02 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_alter_orderbooking_applied_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooking',
            name='is_taken',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]