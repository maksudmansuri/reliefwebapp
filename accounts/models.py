from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db import models
from django.db.models.fields import AutoField
from django.db.models.signals import post_save
from django.dispatch import receiver
# from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.validators import RegexValidator
from django.db.models import Q
# Create your models here.
# class CustomUser(AbstractUser): 
#     user_type_data=((1,"HOD"),(2,"Staff"),(3,"Customer"))
#     user_type=models.CharField(choices=user_type_data,max_length=10)
 
class MyAccountManager(BaseUserManager):
    # create _create_user for mobiel number for facebbook and for google and for userid password so it can be solve your all problem regarding social login/auth
    use_in_migrations = True
    def create_user(self, email, username,password=None):
        if not email:
            raise ValueError("User must have an Email Address")
        if not username:
            raise ValueError("User must have an username ")

        user = self.model(
                email=self.normalize_email(email),
                username=username,
            )
        user.is_active= False
        user.set_password(password)
        user.save(using=self._db)
        print(user)

        return user

    def create_phone_user(self, phone,username,email,password=None):
        if not email:
            raise ValueError("User must have an Email Address")

        user = self.model(
                email=self.normalize_email(email),
                phone =phone, 
                username = username, 
               
            )
        user.is_active= True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password,**extra_fields):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
                username=username,  
            )
        
        # phone = "7801925101"
        user.is_active = True
        # user.is_admin = True
        # user_type="0"
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser): 
    email = models.EmailField(verbose_name="email", max_length=254, unique=True,error_messages={'unique':"This email has already been registered."})
    username = models.CharField(max_length=254,unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True,null=True,blank=True)
    last_login = models.DateTimeField(verbose_name="date joined" ,auto_now_add=True,null=True,blank=True)
    # is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name_title   =models.CharField(max_length=256,blank=True,null=True,default="")
    first_name = models.CharField(max_length=254,blank=True,null=True)
    last_name = models.CharField(max_length=254,blank=True,null=True)
    user_type_data=((1,"AdminHOD"),(2,"Hospitals"),(3,"HospitalDoctors"),(4,"Patients"),(5 ,"Labs"),(6 ,"Pharmacy"),(0,"Admin"))
    user_type=models.CharField(choices=user_type_data,max_length=50)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 10 digits allowed.")
    phone           = models.CharField('Phone',validators =[phone_regex], max_length=10, unique = True,null=True)
    is_Mobile_Verified      = models.BooleanField(blank=True, default=False,null=True)
    is_Email_Verified      = models.BooleanField(blank=True, default=False,null=True)
    counter         = models.IntegerField(default=0, blank=True) #OTP counter
    share         = models.FloatField(default=0, blank=True,null=True)
    otp_session_id  = models.CharField(max_length=120, null=True, default = "")
    otp              = models.CharField(max_length=120, null=True, default = "")
    profile_pic         =models.ImageField(max_length=500,null=True,default="")
    profile_pic         =models.ImageField(max_length=500,null=True,default="")
    # force_to_psswd_chngd = models.BooleanField(blank=False, default=True) 
    USERNAME_FIELD = 'email' 

    REQUIRED_FIELDS = ['username',]

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser

    def has_module_perms(self,app_label):
        return True    

    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
 
class PhoneOTP(models.Model):
    
    # id=models.AutoField(primary_key=True)
    # admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    phone_regex     = RegexValidator( regex = r'^\+?1?\d{9,10}$', message ="Phone number must be entered in the format +919999999999. Up to 14 digits allowed.")
    phone           = models.CharField(validators =[phone_regex], max_length=17, unique = True)
    otp             = models.CharField(max_length=9, blank = True, null=True)
    count           = models.IntegerField(default=0, help_text = 'Number of otp_sent')
    validated       = models.BooleanField(default = False, help_text = 'If it is true, that means user have validate otp correctly in second API')
    otp_session_id  = models.CharField(max_length=120,blank = True, null=True, default = "")
    username        = models.CharField(max_length=20, blank = True, null = True, default = None )
    email           = models.CharField(max_length=50, null = True, blank = True, default = None) 
    password        = models.CharField(max_length=100, null = True, blank = True, default = None) 

    

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)   

class Specailist(models.Model): 
    id                              =models.AutoField(primary_key=True)
    category                        =models.CharField(max_length=500,null=True,blank=True,default="Health Tips") 
    specialist_name                 =models.CharField(max_length=500,null=True,blank=True)
    specialist_icon                 =models.ImageField(null=True,default="",blank=True)
    hover_icon                      =models.ImageField(null=True,default="",blank=True)
    app_icon                        =models.ImageField(null=True,default="",blank=True)
    created_at                      =models.DateTimeField(auto_now_add=True)
    updated_at                      =models.DateTimeField(auto_now_add=True)
    objects                         =models.Manager()
    
    def __str__(self):
        return self.specialist_name

    @property
    def get_specialist_icon_url(self):
        if self.specialist_icon and hasattr(self.specialist_icon, 'url'):
            return self.specialist_icon.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    @property
    def get_hover_icon_url(self):
        if self.hover_icon and hasattr(self.hover_icon, 'url'):
            return self.hover_icon.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

# class LabSpecailist(models.Model):
#     id                  =models.AutoField(primary_key=True)
#     specialist_name               =models.CharField(max_length=500,null=True,blank=True)
#     specialist_icon         =models.ImageField(upload_to="Lab/specialist/images",max_length=500,null=True,default="")
#     created_at          =models.DateTimeField(auto_now_add=True)
#     updated_at          =models.DateTimeField(auto_now_add=True)
#     objects             =models.Manager()

# class PharmacySpecailist(models.Model):
#     id                  =models.AutoField(primary_key=True)
#     specialist_name               =zmodels.CharField(max_length=500,null=True,blank=True)
#     specialist_icon         =models.ImageField(upload_to="Pharmacy/specialist/images",max_length=500,null=True,default="")
#     created_at          =models.DateTimeField(auto_now_add=True)
#     updated_at          =models.DateTimeField(auto_now_add=True)
#     objects             =models.Manager()

class AdminHOD(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
 
class Hospitals(models.Model): 
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")
    hopital_name        =models.CharField(max_length=500,default="",null=True)
    about               =models.TextField(blank=True,null=True,default="")
    # registration_number =models.DateField(blank=True,null=True,default="")
    address1             =models.CharField(max_length=500,blank=True,null=True,default="")
    address2             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=50,blank=True,null=True,default="")
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    # SPECIALIST_TYPE_CHOICE=((1,"PHYSICIAN"),(2,"SURGEN"),(3,"CARDIOLOGY"),(4,"NEUROLOGISTS"))
    # specialist          =models.CharField(max_length=256,blank=True,null=True,default="",choices=SPECIALIST_TYPE_CHOICE)
    specialist          =models.ForeignKey(Specailist,on_delete=models.CASCADE,blank=True,null=True)
    profile_pic         =models.ImageField(max_length=500,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.ImageField(max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    firm                =models.CharField(max_length=256,blank=True,null=True,default="")
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.admin.username 
    
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    @property
    def get_registration_proof_url(self):
        if self.registration_proof and hasattr(self.registration_proof, 'url'):
            return self.registration_proof.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class HospitalPhones(models.Model):
    id                  =models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,on_delete=models.CASCADE,default="")
    hospital_mobile     =models.CharField(max_length=256,blank=True,null=True,default="")
    hospital_email      =models.CharField(max_length=256,blank=True,null=True,default="")
    is_active           =models.BooleanField(default=False)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
 
class HospitalDoctors(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")   
    name_title          =models.CharField(max_length=256,blank=True,null=True,default="")
    fisrt_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    phone               =models.CharField(max_length=50,default="",blank=True,null=True)
    degree              =models.CharField(max_length=50,default="",blank=True,null=True)
    specialist          =models.ForeignKey(Specailist,on_delete=models.CASCADE,blank=True,null=True,default="")
    about               =models.CharField(max_length=500,default="",blank=True,null=True)
    dob                 =models.DateField(blank=True,null=True)
    alternate_mobile    =models.CharField(max_length=250,blank=True,null=True,default="")
    profile_pic         =models.ImageField(blank=True,null=True)
    gender              =models.CharField(max_length=255,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    opd_charges         =models.FloatField(default=0,blank=True,null=True)
    home_charges        =models.FloatField(default=0,blank=True,null=True)
    emergency_charges    =models.FloatField(default=0,blank=True,null=True)
    online_charges    =models.FloatField(default=0,blank=True,null=True)
    is_virtual_available=models.BooleanField(blank=True,null=True,default=False)   
    is_homevisit_available=models.BooleanField(blank=True,null=True,default=False)   
    is_online           =models.BooleanField(blank=True,null=True,default=False)   
    is_hospital_added   =models.BooleanField(blank=True,null=True,default=True) 
    hospital           =models.ForeignKey(Hospitals, related_name="hospitalstaffdoctors", on_delete=models.CASCADE,blank=True,null=True)
    ssn_id              =models.CharField(max_length=50,default="",blank=True,null=True)
    joindate            =models.DateField(blank=True,null=True,default="2000-01-01") 
    is_deactive         =models.BooleanField(blank=True,null=True,default=False) 
    is_active           =models.BooleanField(blank=True,null=True,default=False) 
    created_at          =models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at          =models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.fisrt_name +" "+ self.last_name

    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    # @property
    # def get_registration_proof_url(self):
    #     if self.registration_proof and hasattr(self.registration_proof, 'url'):
    #         return self.registration_proof.url
    #     else:
    #         return "/static/newstatic/assets/img/icons/male.png"

class Patients(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")
    fisrt_name          =models.CharField(max_length=250,blank=True,null=True,default="")
    last_name           =models.CharField(max_length=250,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    city                =models.CharField(max_length=250,blank=True,null=True,default="")
    state               =models.CharField(max_length=250,blank=True,null=True,default="")
    country             =models.CharField(max_length=250,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    dob                 =models.DateField(blank=True,null=True)
    age                 =models.IntegerField(blank=True,null=True)  
    alternate_mobile    =models.CharField(max_length=250,blank=True,null=True,default="")
    profile_pic         =models.ImageField(blank=True,null=True,default="")
    gender              =models.CharField(max_length=255,null=True,default="")
    bloodgroup          =models.CharField(max_length=255,null=True,default="")
    blood_docation_date                 =models.DateField(blank=True,null=True)
    is_donated           =models.BooleanField(blank=True,null=True,default=False)
    blood_donation           =models.BooleanField(blank=True,null=True,default=False)
    hospital            =models.ForeignKey(Hospitals, on_delete=models.DO_NOTHING,blank=True,null=True,default="")
    doctor            =models.ForeignKey(HospitalDoctors, on_delete=models.DO_NOTHING,blank=True,null=True,default="")
    ID_number           =models.CharField(max_length=250,blank=True,null=True,default="")
    ID_proof            =models.ImageField(blank=True,null=True,default="")
    status              =models.CharField(max_length=250,blank=True,null=True,default="") #Healthy,Weak
    added_by_hospital   =models.BooleanField(blank=True,null=True,default=False)
    added_by_doctor   =models.BooleanField(blank=True,null=True,default=False)
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    created_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at          =models.DateTimeField(auto_now_add=True,null=True,blank=True)
    objects             =models.Manager()
     
    def __str__(self):
        self.is_active =True
        return self.admin.phone 
    
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    @property
    def get_ID_proof_url(self):
        if self.ID_proof and hasattr(self.ID_proof, 'url'):
            return self.ID_proof.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

        
class Labs(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")
    lab_name            =models.CharField(max_length=500,default="",null=True)
    about                =models.TextField(max_length=5000,default="",null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="")
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    specialist          =models.CharField(max_length=256,blank=True,null=True,default="")
    profile_pic         =models.ImageField(max_length=500,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.ImageField( max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin            =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    contact_person      =models.CharField(max_length=256,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.lab_name  
    
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    @property
    def get_registration_proof_url(self):
        if self.registration_proof and hasattr(self.registration_proof, 'url'):
            return self.registration_proof.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class Pharmacy(models.Model):
    id                  =models.AutoField(primary_key=True)
    admin               =models.OneToOneField(CustomUser,on_delete=models.CASCADE,blank=True,null=True,default="")
    pharmacy_name       =models.CharField(max_length=500,default="",null=True)
    registration_number =models.CharField(max_length=50,blank=True,null=True,default="")
    address             =models.CharField(max_length=500,blank=True,null=True,default="")
    pin_code            =models.CharField(max_length=250,blank=True,null=True,default="")
    city                =models.CharField(max_length=50,blank=True,null=True,default="") 
    state               =models.CharField(max_length=50,blank=True,null=True,default="")
    country             =models.CharField(max_length=50,blank=True,null=True,default="")
    landline            =models.CharField(max_length=50,blank=True,null=True,default="")
    specialist          =models.CharField(max_length=256,blank=True,null=True,default="")
    profile_pic         =models.ImageField(max_length=500,null=True,default="")
    about               =models.TextField(max_length=5000,blank=True,null=True,default="")
    is_appiled          =models.BooleanField(blank=True,null=True,default=False)
    is_deactive         =models.BooleanField(blank=True,null=True,default=False)
    is_verified         =models.BooleanField(blank=True,null=True,default=False)
    registration_proof  =models.ImageField(max_length=500,blank=True,null=True,default="")
    establishment_year  =models.DateField(auto_now=False, auto_now_add=False,blank=True,null=True)
    website             =models.URLField(max_length=256,blank=True,null=True,default="")
    linkedin             =models.URLField(max_length=256,blank=True,null=True,default="")
    facebook            =models.URLField(max_length=256,blank=True,null=True,default="")
    instagram           =models.URLField(max_length=256,blank=True,null=True,default="")
    twitter             =models.URLField(max_length=256,blank=True,null=True,default="")
    contact_person      =models.CharField(max_length=256,blank=True,null=True,default="")
    alternate_mobile    =models.CharField(max_length=50,blank=True,null=True,default="")
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)
    objects             =models.Manager()
    
    def __str__(self):
        return self.pharmacy_name  
    
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"
    
    @property
    def get_registration_proof_url(self):
        if self.registration_proof and hasattr(self.registration_proof, 'url'):
            return self.registration_proof.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class UserPayments(models.Model):
    id                  =models.AutoField(primary_key=True)
    patient             =models.ForeignKey(Patients, on_delete=models.CASCADE)
    payment_type        =models.CharField(max_length=50)
    payment_provider    =models.CharField(max_length=50)
    account_info        =models.IntegerField()
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now_add=True)

# class DoctorForHospital(models.Model):
#     id                  =models.AutoField(primary_key=True)
#     hospital            =models.ForeignKey(Hospitals, on_delete=models.CASCADE)
#     doctor              =models.ForeignKey(HospitalDoctors, on_delete=models.CASCADE)
#     created_at          =models.DateTimeField(auto_now_add=True)
#     updated_at          =models.DateTimeField(auto_now_add=True)
#     objects             =models.Manager()
     
#     def __str__(self):
#         return self.hospital.hospital_name

class OPDTime(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    opening_time            =           models.TimeField(max_length=500,blank=True,null=True)
    close_time              =           models.TimeField(max_length=500,blank=True,null=True)
    break_start_time        =           models.TimeField(max_length=500,blank=True,null=True)
    break_end_time          =           models.TimeField(max_length=500,blank=True,null=True)
    monday                              =models.CharField(max_length=500,default="",blank=True,null=True) 
    tuesday                             =models.CharField(max_length=500,default="",blank=True,null=True) 
    wednesday                           =models.CharField(max_length=500,default="",blank=True,null=True) 
    thursday                            =models.CharField(max_length=500,default="",blank=True,null=True) 
    friday                              =models.CharField(max_length=500,default="",blank=True,null=True) 
    saturday                            =models.CharField(max_length=500,default="",blank=True,null=True) 
    sunday                              =models.CharField(max_length=500,default="",blank=True,null=True)
    is_active               =           models.BooleanField(blank=True,null=True,default=False)
    created_at              =           models.DateTimeField(auto_now=True)
    updated_at              =           models.DateTimeField(auto_now=True)
    objects                 =           models.Manager()
 
@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Hospitals.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==3:
            HospitalDoctors.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==4:
            Patients.objects.get_or_create(admin=instance)
        if instance.user_type==5:
            Labs.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
        if instance.user_type==6:
            Pharmacy.objects.create(admin=instance)
            OPDTime.objects.create(user=instance)
    # else:
    #     if instance.user_type==1:
    #         AdminHOD.objects.create(admin=instance)
    #     if instance.user_type==2:
    #         Hospitals.objects.create(admin=instance)
    #         OPDTime.objects.create(user=instance)
    #     if instance.user_type==3:
    #         HospitalDoctors.objects.create(admin=instance)
    #         OPDTime.objects.create(user=instance)
    #     if instance.user_type==4:
    #         Patients.objects.get_or_create(admin=instance)
    #     if instance.user_type==5:
    #         Labs.objects.create(admin=instance)
    #         OPDTime.objects.create(user=instance)
    #     if instance.user_type==6:
    #         Pharmacy.objects.create(admin=instance)
    #         OPDTime.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.hospitals.save()
    if instance.user_type==3:
        instance.hospitaldoctors.save()
    if instance.user_type==4:
        instance.patients.save()        
    if instance.user_type==5:
        instance.labs.save()
    if instance.user_type==6:
        instance.pharmacy.save()