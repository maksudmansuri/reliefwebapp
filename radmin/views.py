from django.contrib import messages
from django.http import response
from django.http.request import HttpRequest
from patient.models import Booking, LabTest, OrderBooking, Orders, PicturesForMedicine, Slot
from django.core.files.storage import FileSystemStorage
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect, JsonResponse
from hospital.models import ContactPerson, HospitalMedias, HospitalStaffDoctorSchedual, HospitalStaffDoctors, Insurances, ServiceAndCharges, TimeSlot
from accounts.models import CustomUser, HospitalPhones, Hospitals, Labs, Patients, Pharmacy, Specailist
from django.shortcuts import get_object_or_404, render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Q 

from radmin.models import City, Country, State
# Create your views here.
   
class indexListView(ListView):
    model = Hospitals
    template_name = "radmin/newindex.html" 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["labs_list"] = Labs.objects.all() 
        context["pharmacy_list"] = Pharmacy.objects.all() 
        patients = Patients.objects.all()
        patients_list = []
        for patient in patients:
            total_apt =  OrderBooking.objects.filter(patient = patient.admin).count() 
            patients_list.append({'total_apt':total_apt,'patient':patient})
        context["patient_list"] = patients_list
        return context
    
"""
Hospital Specialist Categories
"""
class AddHospitalSpecialistView(SuccessMessageMixin,CreateView):
    
    def get(self, request, *args, **kwargs):      
        speciallist=Specailist.objects.all()
        param={'speciallists':speciallist}
        return render(request,"radmin/specialities.html",param)
    
    def post(self, request, *args, **kwargs):
        specialist_name=request.POST.get("specialist_name")
        specialist_icon=request.FILES.get("specialist_icon")
        hover_icon=request.FILES.get("hover_icon")
       
        fs=FileSystemStorage()
        filename1=fs.save(specialist_icon.name,specialist_icon)
        profile_pic_url=fs.url(filename1)
        fs1=FileSystemStorage()
        filename2=fs1.save(hover_icon.name,hover_icon)
        hover_icon_url=fs1.url(filename2)
        try:
            specailist = Specailist(specialist_name=specialist_name,specialist_icon=profile_pic_url,hover_icon=hover_icon_url)
            specailist.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
        messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        return HttpResponseRedirect(reverse("specialist_hospital")) 

def updateHospitalSpecialist(request,id):
    specialist_name=request.POST.get("specialist_name")
    specialist_icon=request.FILES.get("specialist_icon")
    hover_icon=request.FILES.get("hover_icon")
    print(specialist_icon,specialist_name)
    
    try: 
        specailist = get_object_or_404(Specailist,id=id)
        specailist.specialist_name=specialist_name
        if specialist_icon:
            fs=FileSystemStorage()
            filename1=fs.save(specialist_icon.name,specialist_icon)
            profile_pic_url=fs.url(filename1)
            specailist.specialist_icon=profile_pic_url
        if hover_icon:
            fs1=FileSystemStorage()
            filename2=fs1.save(hover_icon.name,hover_icon)
            hover_icon_url=fs1.url(filename2)
            specailist.hover_icon=hover_icon_url
        specailist.save()
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
    messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
    return HttpResponseRedirect(reverse("specialist_hospital")) 

def deleteHospitalSpecialist(request,id):
    specailist = get_object_or_404(Specailist,id=id)
    specailist.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("specialist_hospital")) 
 
"""
Hospitals All Views
"""

class HospitalallViews(ListView):
    model = Hospitals
    template_name = "radmin/hospital_all.html" 

def HospitalActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def HospitalDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def HospitalDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))


"""
Patients All Views
"""

class PatientAllViews(ListView):
    model = Patients
    template_name = "radmin/patient_all.html" 

def PatientActivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def PatientDeactivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PatientDelete(request,id):
    hospital=Patients.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))


"""
Labs All Views
"""

class LabsAllViews(ListView):
    model = Labs
    template_name = "radmin/laboratory_all.html" 

def LabsActivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def LabsDeactivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def LabsDelete(request,id):
    hospital=Labs.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))

"""
Pharmacy All Views
"""

class PharmacyAllViews(ListView):
    model = Pharmacy
    template_name = "radmin/pharmacy_all.html" 

def PharmacyActivate(request,id):
    hospital=Pharmacy.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def PharmacyDeactivate(request,id):
    hospital=Pharmacy.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PharmacyDelete(request,id):
    hospital=Pharmacy.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))


"""
Accident All Views
"""

class AccidentAllViews(ListView):
    model = Hospitals
    template_name = "radmin/accident_all.html" 

def AccidentActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_accident_admin"))

def AccidentDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_accident_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def AccidentDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_accident_admin"))


def hospitalUpdateView(request): 
    return render(request,"radmin/doctor_add.html")
 
def hospitalDeleteView(request): 
    return render(request,"radmin/doctor_add.html")

"""
Appointment all view
"""
class AppointmentListView(ListView):
    model = OrderBooking
    template_name = "radmin/appoinment.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["hos_apt"] = OrderBooking.objects.filter(booking_for = "H") 
        context["labs_apt"] = OrderBooking.objects.filter(booking_for = "L") 
        context["pharmacy_apt"] = OrderBooking.objects.filter(booking_for = "P") 
        return context

class HosAppointmentAllViews(ListView):
    model = Booking
    template_name = "radmin/appointment_hospital_all.html"

class PhaAppointmentAllViews(ListView):
    model = PicturesForMedicine
    template_name = "radmin/appointment_pharmacy_all.html"
 
class LabsAppointmentAllViews(ListView):
    def get(self, request, *args, **kwargs):
        allslot = Slot.objects.filter(is_active=True)
        allslot_list = []
        for slots in allslot:
            labtest = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtest':labtest})
        param = {'allslot_list':allslot_list}
        return render(request,"radmin/appointment_labs_all.html",param)

"""
Profile of Hospital Labs Pharmacy Patient
"""
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hospital = get_object_or_404(Hospitals,admin__is_active=True,is_verified=True,is_deactive=False,id=hosital_id)
        doctors = HospitalStaffDoctors.objects.filter(is_active=True,hospital=hospital)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
        hospitalstaffdoctor_list = []
        for hospitalstaffdoctor in doctors:
            hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
            opd_time = []
            for dcsh in hospitalstaffdoctorschedual:
                if dcsh.work == "OPD":
                    shift = dcsh.shift
                    start_time = dcsh.start_time
                    end_time = dcsh.end_time
                opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
            hospitalstaffdoctor_list.append({'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time})
        param = {'hospital':hospital,'hospitalstaffdoctor_list':hospitalstaffdoctor_list,'hospitalservice':hospitalservice}  
        return render(request,"radmin/hospital_profile.html",param)

class DoctorsBookAppoinmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        hospitalstaffdoctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=hositaldcotorid_id)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
      
        
        hospitalstaffdoctorschedual =HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        opd_time = []
        for dcsh in hospitalstaffdoctorschedual:
            if dcsh.work == "OPD":
                shift = dcsh.shift
                start_time = dcsh.start_time
                end_time = dcsh.end_time
            opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
        
        param = {'hospital':hospital,'hospitalservice':hospitalservice,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time}  
        return render(request,"radmin/doctor_profile.html",param)
    
class LabDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        lab = get_object_or_404(Labs,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)
        services = ServiceAndCharges.objects.filter(user=lab.admin)        
        param = {'lab':lab,'services':services}  
        return render(request,"radmin/lab_profile.html",param)

class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        pharmacy = get_object_or_404(Pharmacy,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)   

        param = {'pharmacy':pharmacy}  
        return render(request,"radmin/pharmacy_profile.html",param)

class PatientDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        patient_id=kwargs['id']
        patient = get_object_or_404(Patients,admin__is_active=True,id=patient_id)
        slotbook = Slot.objects.filter(patient=patient.admin)
        allslot_list = []
        for slots in slotbook:
            labtests = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtests':labtests})
        booking = Booking.objects.filter(patient=patient.admin) 

        param = {'patient':patient,'allslot_list':allslot_list,'booking':booking}  
        return render(request,"radmin/patient_profile.html",param)


"""
Add Location country state and city
"""
class AddCountriesView(SuccessMessageMixin,CreateView):
    
    def get(self, request, *args, **kwargs):      
        countries=Country.objects.all()
        states=State.objects.all()
        cities=City.objects.all()
        state_country_wise_list =[]
        for country in countries:
            state_list = State.objects.filter(country=country)
            state_country_wise_list.append({'country':country,'state_list':state_list})
        param={'countries':countries,'states':states,'cities':cities,'state_country_wise_list':state_country_wise_list}
        return render(request,"radmin/add-location.html",param)
    
    def post(self, request, *args, **kwargs):
        area = request.POST.get("area")
        if area == "country":
            country_name=request.POST.get("country_name")
            try:
                country = Country(country_name=country_name)
                country.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        if area == "state":
            state_name=request.POST.get("state_name")
            country=request.POST.get("country")
            print(country)
            country_name = get_object_or_404(Country,id=country)
            try:
                state = State(state_name=state_name,country=country_name)
                state.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        if area == "city":
            city_name=request.POST.get("city_name")
            state=request.POST.get("state")           
            # country=request.POST.get("country")
            # print(city_name,state,country)
            state_name = get_object_or_404(State,id=state) 
            country_name = get_object_or_404(Country,id=state_name.country.id)
            try:
                state = City(city_name=city_name,state=state_name,country=country_name)
                state.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")     
        return HttpResponseRedirect(reverse("loaction_area")) 

def deleteCountry(request,id):
    country = get_object_or_404(Country,id=id)
    country.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

def deleteState(request,id):
    state = get_object_or_404(State,id=id)
    state.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

def deleteCity(request,id):
    city = get_object_or_404(City,id=id)
    city.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

class TimeSlotView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        time_slots = TimeSlot.objects.all().order_by('schedule')
        timeslots_15s = TimeSlot.objects.filter(schedule_type="15")
        timeslots_30s = TimeSlot.objects.filter(schedule_type="30")
        timeslots_45s = TimeSlot.objects.filter(schedule_type="45")
        timeslots_60s = TimeSlot.objects.filter(schedule_type="60")
        param={'timeslots_15s':timeslots_15s,'timeslots_30s':timeslots_30s,'timeslots_45s':timeslots_45s,'timeslots_60s':timeslots_60s}
        return render(request,"radmin/time-slot.html",param)
 
    def post(self, request, *args, **kwargs):
        session = request.POST.get("session")
        schedule_type = request.POST.get("schedule_type")
        schedule = request.POST.get("schedule")
        schedule_check = TimeSlot.objects.filter(schedule=schedule,schedule_type=str(schedule_type)).count()
        if schedule_check > 0:
            messages.add_message(request,messages.ERROR,"Already Added Time..!")
            return HttpResponseRedirect(reverse("time_slot")) 
        time_slot = TimeSlot(session=str(session),schedule_type=schedule_type,schedule=schedule)
        time_slot.save()
        messages.add_message(request,messages.SUCCESS,"SuccessFully Added")
        return HttpResponseRedirect(reverse('time_slot'))

def deleteTimeSlot(request,id):
    time_slot = get_object_or_404(TimeSlot,id=id)
    time_slot.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("time_slot")) 

# def findState(request):
#     country_id = request.POST.get("country_id")
#     countries=Country.objects.all()
#     states=State.objects.all()
#     findstates=State.objects.filter(country=country_id)
#     cities=City.objects.all()
#     # param={'countries':countries,'states':states,'cities':cities,'findstates':findstates}
#     response = {'findstates':findstates}
#     return  HttpResponse(findstates)


