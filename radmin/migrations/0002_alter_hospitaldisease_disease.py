# Generated by Django 4.0.1 on 2022-01-23 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitaldisease',
            name='disease',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='radmin.disease'),
        ),
    ]
