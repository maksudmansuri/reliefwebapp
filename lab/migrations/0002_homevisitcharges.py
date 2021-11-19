# Generated by Django 3.2.5 on 2021-11-17 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_phoneotp_otp_session_id'),
        ('lab', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeVisitCharges',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('charges', models.FloatField(blank=True, default=0, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.labs')),
            ],
        ),
    ]
