from django.db import models

from accounts.models import CustomUser, Hospitals, Patients
 
# Create your models here.
 

class RatingAndComments(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(CustomUser, related_name="comment_from",on_delete=models.CASCADE)
    HLP = models.ForeignKey(CustomUser,related_name="comment_to", on_delete=models.CASCADE)
    rating = models.IntegerField(null=True,blank=True)
    comment = models.TextField(null=True,blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    objects = models.Manager()

    class Meta:
        ordering = ['-created_date']


