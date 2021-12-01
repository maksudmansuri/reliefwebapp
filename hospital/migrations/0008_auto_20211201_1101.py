# Generated by Django 3.2.5 on 2021-12-01 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_alter_doctorschedule_doctor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='doctorschedule',
            options={'ordering': ['scheduleDate']},
        ),
        migrations.AddField(
            model_name='hospitalstaffdoctors',
            name='online_charges',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
