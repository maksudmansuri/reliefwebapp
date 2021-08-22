# Generated by Django 3.2.5 on 2021-08-22 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210822_1400'),
        ('hospital', '0016_auto_20210822_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalStaffDoctorSchedual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('days', models.DateTimeField(blank=True, default='', max_length=50, null=True)),
                ('shift', models.CharField(blank=True, choices=[('Morning', 'Morning'), ('Evening', 'Evening'), ('Full_Day', 'Full_Day')], default='', max_length=50, null=True)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('end_time', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
                ('hospitalstaffdoctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitalstaffdoctors')),
            ],
        ),
    ]
