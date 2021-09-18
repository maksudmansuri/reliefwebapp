# Generated by Django 3.2.5 on 2021-09-09 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('department_head', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('department_name', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('mobile', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalStaffDoctors',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(default='', max_length=254)),
                ('ssn_id', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('joindate', models.DateField(blank=True, default='', null=True)),
                ('is_virtual_available', models.BooleanField(blank=True, default=False, null=True)),
                ('is_online', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaldoctors')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='RoomOrBadTypeandRates',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('room_type', models.CharField(blank=True, choices=[(1, 'A.C'), (2, 'Non-A.C'), (3, 'General')], default='', max_length=50, null=True)),
                ('rooms_price', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='Insurances',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('insurance_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('insurance_name', models.CharField(blank=True, choices=[(1, 'CashLess'), (2, 'No Cahsless')], default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalTreatments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('treatment_name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('treatment_rate', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='hospital.departments')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitaldoctors')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalStaffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_title', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('mobile', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('ssn_id', models.IntegerField(default=1)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalStaffDoctorSchedual',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('shift', models.CharField(blank=True, choices=[('Morning', 'Morning'), ('Noon', 'Noon'), ('Evening', 'Evening'), ('All-Day', 'All-Day')], default='', max_length=50, null=True)),
                ('monday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('tuesday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('wednesday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('thursday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('friday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('saturday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('sunday', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('work', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
                ('hospitalstaffdoctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitalstaffdoctors')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalsPatients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_title', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('address', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('city', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('state', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('country', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('zip_Code', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('age', models.CharField(blank=True, default='', max_length=25, null=True)),
                ('phone', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('email', models.EmailField(blank=True, default='', max_length=254, null=True)),
                ('treatment', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('ID_number', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('ID_proof', models.FileField(blank=True, default='', null=True, upload_to='patients/profile/images')),
                ('status', models.CharField(blank=True, default='', max_length=250, null=True)),
                ('gender', models.CharField(default='', max_length=255, null=True)),
                ('add_notes', models.TextField(blank=True, default='', null=True)),
                ('added_by_hospital', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalServices',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('service_name', models.CharField(blank=True, default='', max_length=500, null=True)),
                ('service_charge', models.FloatField(blank=True, default=0.0, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalRooms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('floor', models.CharField(blank=True, default='', max_length=50, null=True)),
                ('room_no', models.CharField(blank=True, default=1, max_length=50, null=True)),
                ('occupied', models.BooleanField(blank=True, default=False, null=True)),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hospital.departments')),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
                ('room', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hospital.roomorbadtypeandrates')),
            ],
        ),
        migrations.CreateModel(
            name='HospitalMedias',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('media_type', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('media_content', models.FileField(blank=True, choices=[(1, 'Image'), (2, 'Video')], default='', null=True, upload_to='')),
                ('media_desc', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.AddField(
            model_name='departments',
            name='hospital_staff_doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.hospitalstaffdoctors'),
        ),
        migrations.CreateModel(
            name='DepartmentPhones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('mobile', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('department', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='hospital.departments')),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name_title', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('mobile', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('email', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('hospital', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accounts.hospitals')),
            ],
        ),
    ]
