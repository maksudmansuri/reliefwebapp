# Generated by Django 4.0.1 on 2022-01-26 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_hospitaldoctors_admin_hospitaldoctors_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specailist',
            name='app_icon',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='specailist',
            name='hover_icon',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='specailist',
            name='specialist_icon',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
    ]