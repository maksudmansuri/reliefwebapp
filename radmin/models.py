from pyexpat import model
from django.db import models

from accounts.models import CustomUser, HospitalDoctors, Hospitals

class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=50,null=True,blank=True,default="")
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

class State(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    state_name = models.CharField(max_length=50,null=True,blank=True,default="")
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

class City(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,null=True,blank=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    city_name = models.CharField(max_length=50,null=True,blank=True,default="")
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()
 
class DonorRequest(models.Model):
    id = models.AutoField(primary_key=True)
    reqestpersoned = models.ForeignKey(CustomUser,related_name="request_from",on_delete=models.CASCADE,null=True,blank=True)#who request
    forpersoned = models.ForeignKey(CustomUser,related_name="request_to",on_delete=models.CASCADE,null=True,blank=True)#who request
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

class Disease(models.Model):
    id =            models.AutoField(primary_key=True)
    name =          models.CharField(max_length=50,null=True,blank=True,default="")
    desc =              models.CharField(max_length=50,null=True,blank=True,default="")
    d_icon                 =models.ImageField(max_length=500,null=True,default="")
    is_active           =models.BooleanField(blank=True,null=True,default=False)
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

    @property
    def get_d_icon_url(self):
        if self.d_icon and hasattr(self.d_icon, 'url'):
            return self.d_icon.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class HospitalDisease(models.Model):
    id =            models.AutoField(primary_key=True)
    hospital            =models.ForeignKey(Hospitals,related_name="hospitaldisease", on_delete=models.DO_NOTHING,blank=True,null=True,default="")
    doctor            =models.ForeignKey(HospitalDoctors,related_name="hospitaldoctors_disease", on_delete=models.DO_NOTHING,blank=True,null=True,default="")
    disease                 =models.ForeignKey(Disease,on_delete=models.CASCADE,blank=True,null=True,default="")
    created_at                   =models.DateTimeField(auto_now=True)
    updated_at                   =models.DateTimeField(auto_now=True)
    objects                      =models.Manager()

