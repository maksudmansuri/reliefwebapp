# Generated by Django 4.0.1 on 2022-01-13 09:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hospital', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('media_content', models.FileField(blank=True, choices=[(1, 'Image'), (2, 'Video')], default='', null=True, upload_to='')),
                ('media_desc', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LabSchedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('scheduleDate', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('is_booked', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lab', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.labs')),
                ('timeslot', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='hospital.timeslot')),
            ],
            options={
                'ordering': ['scheduleDate'],
            },
        ),
        migrations.CreateModel(
            name='HomeVisitCharges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('charges', models.FloatField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.labs')),
            ],
        ),
    ]
