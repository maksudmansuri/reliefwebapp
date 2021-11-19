from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View

from django.contrib import messages

from accounts.models import Hospitals, Labs, Pharmacy
from patient.models import PicturesForMedicine
# Create your views here.

class FrontView(View):
    def get(self, request, *args, **kwargs):
       
        hospitals=Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        labs=Labs.objects.filter(admin__is_active=True,is_verified = True)
        pharmacys=Pharmacy.objects.filter(admin__is_active=True,is_verified = True)
        # departments = Departments.objects.filter(hospital=hospital)
        print(hospitals)
        param={'hospitals':hospitals,'labs':labs,'pharmacys':pharmacys}
        return render(request,"front/index.html",param)
