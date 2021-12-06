import json
from django.contrib.auth.decorators import login_required
from django.contrib.messages import views
from django.core import paginator
from django.db.models.base import Model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View,ListView,DetailView

from django.contrib import messages
from django.db.models import Q
from chat.models import Notification
from accounts.models import AdminHOD, Hospitals, Labs, Pharmacy, Specailist
from accounts.views import send_otp
from hospital.models import AmbulanceDetails, Blog, DoctorSchedule, HospitalMedias, HospitalRooms, HospitalStaffDoctors, ServiceAndCharges
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime,timedelta
from django.db.models import Avg, Max, Min, Sum
from lab.models import LabSchedule, Medias

from patient.models import ForSome, OrderBooking, phoneOPTforoders
# Create your views here.
  
class FrontView(View):
    def get(self, request, *args, **kwargs):
        
        hospitals=Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        labs=Labs.objects.filter(admin__is_active=True,is_verified = True)
        pharmacys=Pharmacy.objects.filter(admin__is_active=True,is_verified = True)
        specilist = Specailist.objects.all()
        blogs = Blog.objects.filter(is_active=True)
        # departments = Departments.objects.filter(hospital=hospital)
        print(hospitals) 
        param={'hospitals':hospitals,'labs':labs,'pharmacys':pharmacys,'specilist':specilist,'blogs':blogs}
        return render(request,"front/index.html",param)

class BlogListView(ListView):
    model = Blog
    template_name = "front/blog-grid.html"
    paginate_by = 3
    queryset = Blog.objects.filter(is_active=True)

class BlogDetailsView(DetailView):
    model = Blog
    template_name = "front/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_list"] = Blog.objects.filter(is_active = True) 
        return context

"""Searcch all"""
class SearchOnlineHospitalView(ListView):
    model = HospitalStaffDoctors
    template_name = "front/online-doctor-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            doctors=HospitalStaffDoctors.objects.filter( Q(is_virtual_available=True,is_active=True) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            doctors=HospitalStaffDoctors.objects.filter(is_virtual_available=True,is_active=True).order_by(order_by)
        return doctors
    
    def get_context_data(self,**kwargs):
        context=super(SearchOnlineHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["doctors_number"]=HospitalStaffDoctors.objects.filter(is_virtual_available=True,is_active=True).count()
        context["all_table_fields"]=HospitalStaffDoctors._meta.get_fields()
        return context

class SearchHomeVisitHospitalView(ListView):
    model = HospitalStaffDoctors
    template_name = "front/homevisit-doctor-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            doctors=HospitalStaffDoctors.objects.filter( Q(is_homevisit_available=True,is_active=True) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            doctors=HospitalStaffDoctors.objects.filter(is_homevisit_available=True,is_active=True).order_by(order_by)
        return doctors
    
    def get_context_data(self,**kwargs):
        context=super(SearchHomeVisitHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["doctors_number"]=HospitalStaffDoctors.objects.filter(is_homevisit_available=True,is_active=True).count()
        context["all_table_fields"]=HospitalStaffDoctors._meta.get_fields()
        return context

class SearchAmbulanceHospitalView(ListView):
    model = AmbulanceDetails
    template_name = "front/ambulance-search.html"
  

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            ambulances=AmbulanceDetails.objects.filter( Q(is_active=True,occupied=False) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            ambulances=AmbulanceDetails.objects.filter(is_active=True,occupied=False).order_by(order_by)
        return ambulances
    
    def get_context_data(self,**kwargs):
        context=super(SearchAmbulanceHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["total_ambulance"]=AmbulanceDetails.objects.filter(is_active=True,occupied=False).count()
        context["all_table_fields"]=AmbulanceDetails._meta.get_fields()
        return context


class SearchLabView(ListView):
    model = Labs
    template_name = "front/lab-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            labs=Labs.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(lab_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(address__contains=filter_val))).order_by(order_by)
        else:
            labs=Labs.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        
        lab_list = []
        for lab in labs:
            medias = Medias.objects.filter(is_active=True,user=lab.admin)
            services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True)
            lab_list.append({'lab':lab,'medias':medias,'services':services})
        print(lab_list)        
        return lab_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchLabView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["lab_number"]=Labs.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).count()
        context["all_table_fields"]=Labs._meta.get_fields()
        return context

class SearchPharmacyView(ListView):
    pass

class SearchBloodDonorView(ListView):
    pass


class SearchHospitalView(ListView):
    model = Hospitals
    template_name = "front/hospital-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            hospitals=Hospitals.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            hospitals=Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        
        hospital_media_list = []
        for hospital in hospitals:
            print(hospital.admin)
            amount = ServiceAndCharges.objects.filter(user=hospital.admin,service_name = "OPD")
            print(amount)
            medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)
            rooms = HospitalRooms.objects.filter(hospital = hospital,is_active = True).count()
            room_max_price = HospitalRooms.objects.filter(hospital = hospital,is_active = True).aggregate(Max('room__rooms_price'))
            room_min_price = HospitalRooms.objects.filter(hospital = hospital,is_active = True).aggregate(Min('room__rooms_price'))
            ambulances = AmbulanceDetails.objects.filter(hospital=hospital,is_active=True).count()    
            hospital_media_list.append({'hospital':hospital,'medias':medias,'amount':amount,'rooms':rooms,'ambulances':ambulances,'room_max_price':room_max_price,'room_min_price':room_min_price})
        print(hospital_media_list)        
        return hospital_media_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

"""Details View Hospital"""

class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id'] 
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)  
        doctors = HospitalStaffDoctors.objects.filter(is_active=True,hospital=hospital)
        A_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True,occupied=False).count()
        # O_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True,occupied=True).count()
        T_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True).count()
        # T_room = A
        A_ambulances = AmbulanceDetails.objects.filter(hospital=hospital,is_active=True,occupied=False).count()
        T_ambulances = AmbulanceDetails.objects.filter(hospital=hospital,is_active=True).count()
       
        param = {'hospital':hospital,'medias':medias,'doctors':doctors,'A_rooms':A_rooms,'T_rooms':T_rooms,'A_ambulances':A_ambulances,'T_ambulances':T_ambulances}  
        return render(request,"front/new_hospital_details.html",param)

class DoctorsBookAppoinmentViews(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=hositaldcotorid_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,hospital=hospital)
        forsome = ForSome.objects.filter(patient = request.user.patients) 
        token =False
        param = {'hospital':hospital,'doctor':doctor,'doctorschedules':doctorschedules,'token':token,'someones':forsome}  
        return render(request,"front/booking.html",param)
     
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['did'] 
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=doc_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        forsome = ForSome.objects.filter(patient = request.user.patients) 
        print(date,doctor,doctorschedules)
        token = True
        param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token,'someones':forsome}  
        return render(request,"front/booking.html",param)


"""Lab Details"""
class LabDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id'] 
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        medias = Medias.objects.filter(is_active=True,user=lab.admin)  
        services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True)       
        param = {'lab':lab,'medias':medias,'services':services}  
        return render(request,"front/lab_details.html",param)

class LabAppoinmentViews(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id'] 
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        medias = Medias.objects.filter(is_active=True,user=lab.admin)  
        services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True) 
       
        doctorschedules = LabSchedule.objects.filter(lab=lab)
        forsome = ForSome.objects.filter(patient = request.user.patients) 
        token =False 
        param = {'lab':lab,'medias':medias,'services':services,'doctorschedules':doctorschedules,'token':token,'someones':forsome}  
        return render(request,"front/Lab-booking.html",param)
     
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        lab_id=kwargs['id'] 
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        medias = Medias.objects.filter(is_active=True,user=lab.admin)  
        services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True) 
        doctorschedules = LabSchedule.objects.filter(lab=lab,scheduleDate=date)
        print(doctorschedules)       
        # doctorschedules = LabSchedule.objects.filter(lab=lab)
        forsome = ForSome.objects.filter(patient = request.user.patients) 
        token =True 
        param = {'lab':lab,'medias':medias,'services':services,'doctorschedules':doctorschedules,'date':date,'token':token,'someones':forsome}  
        return render(request,"front/lab-booking.html",param)


class InvoiceViews(View):
    def get(self, request, *args, **kwargs):
        id=kwargs['id']
        booking = get_object_or_404(OrderBooking,id=id)
        param ={'booking':booking}
        return render(request,"front/invoice-view.html",param)
 
    