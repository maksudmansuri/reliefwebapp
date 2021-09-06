# Generated by Django 3.2.5 on 2021-09-05 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0025_rename_media_desc_hospitalmedias_media_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalsPatients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('zip_Code', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('age', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('treatment', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('ID_number', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('ID_proof', models.FileField(blank=True, default='', null=True, upload_to='patients/profile/images')),
                ('status', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('gender', models.CharField(default='', max_length=255, null=True)),
                ('add_notes', models.TextField(blank=True, default='', null=True)),
                ('added_by_hospital', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
