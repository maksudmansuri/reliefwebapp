# Generated by Django 4.0.1 on 2022-01-20 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_hospitals_specialist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospitaldoctors',
            old_name='zip_Code',
            new_name='pin_code',
        ),
    ]