from django.db.models.fields import AutoField
from accounts.models import CustomUser, Labs
from django.db import models

from hospital.models import TimeSlot

# Create your models here.

class LabSchedule(models.Model):
    id                  =models.AutoField(primary_key=True)
    lab                 =models.ForeignKey(Labs,on_delete=models.CASCADE,default="",blank=True,null=True)
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
        ordering = ['scheduleDate']

class Medias(models.Model):
    id                      =           models.AutoField(primary_key=True)
    user                    =           models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    media_type              =           models.CharField(max_length=255,blank=True,null=True,default="")
    media_type_choice       =           ((1,"Image"),(2,"Video"))
    media_content           =           models.ImageField(choices=media_type_choice,blank=True,null=True,default="")
    media_desc              =           models.CharField(max_length=255,blank=True,null=True,default="")
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()

    @property
    def get_media_content_url(self):
        if self.media_content and hasattr(self.media_content, 'url'):
            return self.media_content.url
        else:
            return "/static/newstatic/assets/img/icons/male.png"

class HomeVisitCharges(models.Model):
    id                      =           models.AutoField(primary_key=True)
    lab                     =           models.ForeignKey(Labs, on_delete=models.CASCADE)
    charges                 =           models.FloatField(default=0,blank=True,null=True)
    is_active               =           models.BooleanField(default=False)     
    is_default              =           models.BooleanField(default=False)     
    created_date            =           models.DateTimeField(auto_now_add=True)
    updated_at              =           models.DateTimeField(auto_now_add=True)
    objects                 =           models.Manager()
