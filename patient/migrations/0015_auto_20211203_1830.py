# Generated by Django 3.2.5 on 2021-12-03 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0014_auto_20211202_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderbooking',
            name='invoice',
            field=models.FileField(blank=True, default='', null=True, upload_to='booking/invoices'),
        ),
        migrations.AlterField(
            model_name='forsome',
            name='ID_proof',
            field=models.FileField(blank=True, default='', null=True, upload_to='someone/ID/images'),
        ),
        migrations.AlterField(
            model_name='orderbooking',
            name='prescription',
            field=models.FileField(blank=True, default='', max_length=256, null=True, upload_to='booking/prescription'),
        ),
        migrations.AlterField(
            model_name='orderbooking',
            name='store_invoice',
            field=models.FileField(blank=True, default='', max_length=256, null=True, upload_to='booking/store_invoice'),
        ),
        migrations.AlterField(
            model_name='patientfile',
            name='file',
            field=models.FileField(blank=True, default='', null=True, upload_to='patients/documents/file'),
        ),
    ]
