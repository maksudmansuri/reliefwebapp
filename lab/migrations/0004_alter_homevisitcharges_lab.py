# Generated by Django 4.0.1 on 2022-01-25 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_hospitaldoctors_admin_hospitaldoctors_admin_and_more'),
        ('lab', '0003_alter_medias_lab_alter_medias_pharmacy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homevisitcharges',
            name='lab',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='HomeVisitCharges', to='accounts.labs'),
        ),
    ]
