from datetime import time
from os import stat_result
from django.core.files.storage import default_storage
from django.core.validators import RegexValidator

from django.db.models.deletion import DO_NOTHING

from django.db import models

from accounts.models import HospitalDoctors, Hospitals,CustomUser

# Create your models here.  

class TimeSlot(models.Model):
    id                  =models.AutoField(primary_key=True)
    session             =models.CharField(blank=True,null=True,default="",max_length=200)
    schedule_type       =models.CharField(blank=True,null=True,default="",max_length=200)
    schedule            =models.TimeField(auto_now=False, auto_now_add=False,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()

    def __str__(self):
        return str(self.schedule)

class DoctorSchedule(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="",blank=True,null=True)
    doctor              =models.ForeignKey(HospitalDoctors,related_name="schedule", on_delete=models.CASCADE,blank=True,null=True)
    timeslot            =models.ForeignKey(TimeSlot, on_delete=models.CASCADE,blank=True,null=True,default="")
    scheduleDate        = models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    is_booked           =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()

    def __str__(self):
        return str(self.timeslot)
    
    class Meta:
        ordering = ['-scheduleDate']

class HospitalStaffs(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name          =models.CharField(max_length=256,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    ssn_id              =models.IntegerField(default=1)
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.name_title + self.first_name + " " + self.last_name

class HospitalStaffDoctorSchedual(models.Model):
    id                           =models.AutoField(primary_key=True)
    hospital                     =models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    hospitalstaffdoctor          =models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    # SHIFT_CHOICE                 =(("Morning","Morning"),("Noon","Noon"),("Evening","Evening"),("All-Day","All-Day"))
    # DAY_CHOICE                   =(("YES","YES"),("NO","NO"))
    # shift                        =models.CharField(choices=SHIFT_CHOICE, max_length=50,default="",blank=True,null=True)
    monday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    tuesday                      =models.CharField(max_length=500,default="",blank=True,null=True) 
    wednesday                    =models.CharField(max_length=500,default="",blank=True,null=True) 
    thursday                     =models.CharField(max_length=500,default="",blank=True,null=True) 
    friday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    saturday                     =models.CharField(max_length=500,default="",blank=True,null=True) 
    sunday                       =models.CharField(max_length=500,default="",blank=True,null=True) 
    work                         =models.CharField(max_length=500,default="",blank=True,null=True)        
    start_time                   =models.TimeField(auto_now=False,blank=True,null=True)
    end_time                     =models.TimeField(auto_now=False,blank=True,null=True)
    break_time_start             =models.TimeField(auto_now=False,blank=True,null=True)
    break_time_end               =models.TimeField(auto_now=False,blank=True,null=True)
    opd_duration                 =models.IntegerField(blank=True,null=True,default=20)
    is_active                    =models.BooleanField(blank=True,null=True,default=True)
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

class Departments(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    hospital_staff_doctor=models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    department_head     =models.CharField(max_length=256,blank=True,null=True,default="")
    department_name     =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()

    def __str__(self):
        return self.department_name

class RoomOrBadTypeandRates(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    ROOM_TYPE_CHOICE    =((1,"A.C"),(2,"Non-A.C"),(3,"General"))
    room_type           =models.CharField(choices=ROOM_TYPE_CHOICE, max_length=50,default="",blank=True,null=True)
    rooms_price         =models.IntegerField(default=0)
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.room_type

class HospitalRooms(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,related_name="hospitalrooms", on_delete=models.CASCADE,default="")
    department          =models.ForeignKey(Departments,on_delete=models.CASCADE,default="",blank=True,null=True)
    room                =models.ForeignKey(RoomOrBadTypeandRates,on_delete=models.CASCADE,default="")
    floor               =models.CharField(max_length=50,default="",blank=True,null=True)
    room_no             =models.CharField(max_length=50,blank=True,null=True,default=1)    
    occupied            =models.BooleanField(default=False,blank=True,null=True)    
    is_active           =models.BooleanField(default=False,blank=True,null=True)
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.room_no

class ContactPerson(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name          =models.CharField(max_length=256,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=256,blank=True,null=True,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.hospital.hopital_name +" Department of" + self.department

class Insurances(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    insurance_type          =           models.CharField(max_length=255,blank=True,null=True,default="")
    insurance_type_choice   =           ((1,"CashLess"),(2,"No Cahsless"))
    insurance_name          =           models.CharField(choices=insurance_type_choice,blank=True,null=True,default="",max_length=255)
    is_active               =           models.BooleanField(default=False)         
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name

class DepartmentPhones(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    department          =models.ForeignKey(Departments,on_delete=models.CASCADE,default="")
    mobile              =models.CharField(max_length=256,blank=True,null=True,default="")
    email               =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
    
    def __str__(self):
        return self.hospital.hopital_name +" Department of" + self.department

class HospitalMedias(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals,related_name="hospitalmedia",on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,blank=True,null=True,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           models.ImageField(blank=True,null=True,default="")
    media_desc              =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name
    
    @property
    def get_media_content_url(self):
        if self.media_content and hasattr(self.media_content, 'url'):
            return self.media_content.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class HospitalTreatments(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    department              =           models.OneToOneField(Departments, on_delete=models.CASCADE)
    doctor                  =           models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
    treatment_name          =           models.CharField(max_length=255,blank=True,null=True,default="")
    treatment_rate          =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    def __str__(self):
        return self.hospital.hopital_name

# class shiftsDaysTime(models.Model):
#     id = models.AutoField(primary_key=True)
#     number_of_Days = models.IntegerField()
#     shift_start_time = models.TimeField(auto_now=False, auto_now_add=False)
#     shift_end_time = models.TimeField(auto_now=False, auto_now_add=False)

class HospitalsPatients(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals, on_delete=models.DO_NOTHING)
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    age                 =models.CharField(blank=True,null=True,default="",max_length=25)
    phone               =models.CharField(max_length=250,blank=True,null=True,default="")
    email               =models.EmailField(max_length=254,blank=True,null=True,default="")
    treatment           =models.CharField(max_length=250,blank=True,null=True,default="")
    ID_number           =models.CharField(max_length=250,blank=True,null=True,default="")
    ID_proof            =models.ImageField(blank=True,null=True,default="")
    status              =models.CharField(max_length=250,blank=True,null=True,default="")
    gender              =models.CharField(max_length=255,null=True,default="")
    add_notes           =models.TextField(null=True,blank=True,default="")
    added_by_hospital   =models.BooleanField(blank=True,null=True,default=False)
    is_active          =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now=True)
    updated_at          =models.DateTimeField(auto_now=True)
    objects             =models.Manager()
    
    def __str__(self): 
        return self.fisrt_name +" "+ self.last_name
    
    @property
    def get_ID_proof_url(self):
        if self.ID_proof and hasattr(self.ID_proof, 'url'):
            return self.ID_proof.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"


class HospitalServices(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE)
    service_name            =           models.CharField(max_length=500,blank=True,null=True,default="")
    service_charge          =           models.FloatField(blank=True,null=True,default=0.0)
    created_at              =           models.DateTimeField(auto_now=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
    
    def __str__(self): 
        return self.service_name

class ServiceAndCharges(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser,related_name="serviceandcharges_set", on_delete=models.CASCADE)
    service_name            =           models.CharField(max_length=500,blank=True,null=True,default="")
    service_charge          =           models.FloatField(blank=True,null=True,default=0.0)
    is_active               =           models.BooleanField(blank=True,null=True,default=False)
    created_at              =           models.DateTimeField(auto_now=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
    
    def __str__(self): 
        return self.service_name

class AmbulanceDetails(models.Model):  
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals,related_name="hospitalambulance", on_delete=models.CASCADE)
    profile_pic                =           models.ImageField(blank=True,null=True,default="")
    drive_name              =           models.CharField(max_length=500,blank=True,null=True,default="")
    phone_regex             =           RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    drive_number            =            models.CharField('Phone',validators =[phone_regex], max_length=10, unique = True)                                          
    doctor                  =           models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE,blank=True,null=True)
    vehicle_type            =           models.CharField(max_length=500,blank=True,null=True,default="")
    vehicle_number          =           models.CharField(max_length=500,blank=True,null=True,default="")
    charge                  =           models.FloatField(blank=True,null=True,default=0.0)
    occupied                =           models.BooleanField(default=False,blank=True,null=True)
    Area                    =           models.CharField(max_length=500,blank=True,null=True,default="")
    is_active               =           models.BooleanField(blank=True,null=True,default=False)
    created_at              =           models.DateTimeField(auto_now=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
    
    def __str__(self): 
        return self.vehicle_number
    
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
class Blog(models.Model):
    id                      =           models.AutoField(primary_key=True)
    hospital                =           models.ForeignKey(Hospitals, on_delete=models.CASCADE,blank=True,null=True)
    doctor                  =           models.ForeignKey(HospitalDoctors,related_name="hospitaldoctors_blogs", on_delete=models.CASCADE,blank=True,null=True)
    blog_title              =           models.CharField(max_length=500,blank=True,null=True,default="")
    blog_content            =           models.TextField(max_length=5000,blank=True,null=True,default="")
    blog_image              =           models.ImageField(blank=True,null=True,default="")
    is_active               =           models.BooleanField(blank=True,null=True,default=False)
    created_at              =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
     
    def __str__(self): 
        return self.blog_title
    
    @property
    def get_blog_image_url(self):
        if self.blog_image and hasattr(self.blog_image, 'url'):
            return self.blog_image.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    class Meta:
        ordering = ['created_at']

