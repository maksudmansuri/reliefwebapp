# Generated by Django 4.0.1 on 2022-01-13 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp',
            name='order_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
