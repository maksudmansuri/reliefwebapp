# Generated by Django 3.2.5 on 2021-08-18 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210817_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminhod',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_pic',
            field=models.FileField(default='', max_length=500, null=True, upload_to='user/profile_pic'),
        ),
    ]
