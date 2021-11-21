from django.db import models


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
 
   