# Generated by Django 3.2.5 on 2021-11-19 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_phoneotp_otp_session_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specailist',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('specialist_name', models.CharField(blank=True, max_length=500, null=True)),
                ('specialist_icon', models.FileField(default='', max_length=500, null=True, upload_to='Hospital/specialist/images/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
