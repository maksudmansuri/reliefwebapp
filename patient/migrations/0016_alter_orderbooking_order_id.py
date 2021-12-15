# Generated by Django 3.2.5 on 2021-12-03 13:05

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_auto_20211203_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbooking',
            name='order_id',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
    ]