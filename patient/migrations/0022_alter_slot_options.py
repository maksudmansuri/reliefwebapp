# Generated by Django 3.2.5 on 2021-10-25 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0021_delete_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slot',
            options={'ordering': ['-updated_at']},
        ),
    ]