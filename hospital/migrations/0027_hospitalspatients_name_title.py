# Generated by Django 3.2.5 on 2021-09-05 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0026_hospitalspatients'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalspatients',
            name='name_title',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
    ]