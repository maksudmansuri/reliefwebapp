# Generated by Django 4.0.1 on 2022-01-25 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hospital', '0003_alter_serviceandcharges_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceandcharges',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serviceandcharges_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
