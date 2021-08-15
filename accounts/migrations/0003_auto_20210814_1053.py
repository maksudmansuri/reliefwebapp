# Generated by Django 3.2.5 on 2021-08-14 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_hospitalphone'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HospitalPhone',
            new_name='HospitalPhones',
        ),
        migrations.RenameModel(
            old_name='userPayment',
            new_name='UserPayments',
        ),
        migrations.AlterField(
            model_name='patients',
            name='address',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='alternate_mobile',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='city',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='country',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='dob',
            field=models.DateField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='fisrt_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='gender',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='profile_pic',
            field=models.FileField(blank=True, default='', null=True, upload_to='patients/profile/images'),
        ),
        migrations.AlterField(
            model_name='patients',
            name='state',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='zip_Code',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
        migrations.CreateModel(
            name='HospitalDoctors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fisrt_name', models.CharField(blank=True, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=250, null=True)),
                ('state', models.CharField(blank=True, max_length=250, null=True)),
                ('country', models.CharField(blank=True, max_length=250, null=True)),
                ('zip_Code', models.CharField(blank=True, max_length=250, null=True)),
                ('phone', models.CharField(max_length=50)),
                ('dob', models.DateField(blank=True, null=True)),
                ('alternate_mobile', models.CharField(blank=True, max_length=250, null=True)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='patients/profile/images')),
                ('gender', models.CharField(max_length=255, null=True)),
                ('is_appiled', models.BooleanField(blank=True, default=False, null=True)),
                ('is_verified', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
