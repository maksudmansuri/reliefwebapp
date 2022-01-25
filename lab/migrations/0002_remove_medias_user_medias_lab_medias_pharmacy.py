# Generated by Django 4.0.1 on 2022-01-25 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_hospitals_specialist'),
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medias',
            name='user',
        ),
        migrations.AddField(
            model_name='medias',
            name='lab',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.labs'),
        ),
        migrations.AddField(
            model_name='medias',
            name='pharmacy',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.pharmacy'),
        ),
    ]
