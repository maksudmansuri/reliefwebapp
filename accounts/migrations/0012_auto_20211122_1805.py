# Generated by Django 3.2.5 on 2021-11-22 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_labspecailist_pharmacyspecailist'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LabSpecailist',
        ),
        migrations.DeleteModel(
            name='PharmacySpecailist',
        ),
        migrations.AddField(
            model_name='specailist',
            name='hover_icon',
            field=models.FileField(default='', max_length=500, null=True, upload_to='Hospital/specialist/images/%Y/%m/%d/'),
        ),
    ]
