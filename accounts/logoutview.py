from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse
from hospital.models import Insurances,HospitalRooms,HospitalMedias,HospitalStaffs,HospitalStaffDoctorSchedual
from accounts.models import Hospitals,HospitalDoctors,HospitalPhones
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("front_home"))

class hospitalProfileViews(SuccessMessageMixin,DetailView):
    def get(self, request):
        try: 
            hospital = Hospitals.objects.get(admin=request.user.id)
            contacts = HospitalPhones.objects.filter(hospital=hospital)
            insurances = Insurances.objects.filter(hospital=hospital)
            param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
            return render(request,"hospital/hospital_profile.html",param)
        except Exception as e:
            return HttpResponse(e)