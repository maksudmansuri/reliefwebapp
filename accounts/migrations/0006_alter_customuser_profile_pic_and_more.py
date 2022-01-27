# Generated by Django 4.0.1 on 2022-01-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_specailist_app_icon_alter_specailist_hover_icon_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_pic',
            field=models.ImageField(default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='hospitals',
            name='profile_pic',
            field=models.ImageField(default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='hospitals',
            name='registration_proof',
            field=models.ImageField(blank=True, default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='labs',
            name='profile_pic',
            field=models.ImageField(default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='labs',
            name='registration_proof',
            field=models.ImageField(blank=True, default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='patients',
            name='ID_proof',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='patients',
            name='profile_pic',
            field=models.ImageField(blank=True, default='', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='profile_pic',
            field=models.ImageField(default='', max_length=500, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='registration_proof',
            field=models.ImageField(blank=True, default='', max_length=500, null=True, upload_to=''),
        ),
    ]