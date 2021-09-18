# Generated by Django 3.2.5 on 2021-09-18 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pharmacy',
            name='Landline',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='about',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='address',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='contact_number',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='contact_person',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='country',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='establishment_year',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='linkdin',
            field=models.URLField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='profile_pic',
            field=models.FileField(default='', max_length=500, null=True, upload_to='Pharmacist/profile'),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='registration_number',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='registration_proof',
            field=models.FileField(blank=True, default='', max_length=500, null=True, upload_to='hospital/documents'),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='specialist',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='state',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='pharmacy',
            name='website',
            field=models.URLField(blank=True, default='', max_length=256, null=True),
        ),
    ]
