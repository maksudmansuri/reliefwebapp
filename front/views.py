from django.contrib.auth.decorators import login_required
from django.contrib.messages import views
from django.core import paginator
from django.db.models.base import Model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View,ListView,DetailView
from django.contrib import messages
from django.db.models import Q
import pytz
from chat.models import Notification
from accounts.models import AdminHOD, CustomUser, HospitalDoctors, Hospitals, Labs, Patients, Pharmacy, Specailist
from accounts.views import send_otp
from relief import settings
IST = pytz.timezone('Asia/Kolkata')
from front.models import RatingAndComments
from hospital.models import AmbulanceDetails, Blog, DoctorSchedule, HospitalMedias, HospitalRooms, Insurances, ServiceAndCharges
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime,timedelta
from django.db.models import Avg, Max, Min, Sum
from lab.models import HomeVisitCharges, LabSchedule, Medias
from patient.models import ForSome, NewLabTest, OrderBooking, Temp, TreatmentReliefPetient, phoneOPTforoders
from radmin.models import DonorRequest, HospitalDisease
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, message

# Create your views here.
  
class FrontView(View):
    def get(self, request, *args, **kwargs):        
        hospitals=Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        hospitals_list = []
        for hospital in hospitals:
            total_cmns = RatingAndComments.objects.filter(HLP =hospital.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =hospital.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            hospitals_list.append({'hospital':hospital,'rating':rating,'total_cmns':total_cmns})
        doctors=HospitalDoctors.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        #Doctor with ratings
        doctor_list = []
        for doctor in doctors:
            total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            doctor_list.append({'doctor':doctor,'rating':rating,'total_cmns':total_cmns})
        print(doctor_list)
        labs=Labs.objects.filter(admin__is_active=True,is_verified = True)
        labs_list = []
        for lab in labs:
            total_cmns = RatingAndComments.objects.filter(HLP =lab.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =lab.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            labs_list.append({'lab':lab,'rating':rating,'total_cmns':total_cmns})
        #Pharmac with rating
        pharmacys=Pharmacy.objects.filter(admin__is_active=True,is_verified = True)
        pharmacys_list = []
        for pharmacy in pharmacys:
            total_cmns = RatingAndComments.objects.filter(HLP =pharmacy.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =pharmacy.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            pharmacys_list.append({'pharmacy':pharmacy,'rating':rating,'total_cmns':total_cmns})
        specilist = Specailist.objects.all()
        specilist_list = [] 
        for spc in specilist:
            cet_hospitals = Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False,specialist = spc).count()
            cet_doctors = HospitalDoctors.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False,specialist = spc).count()
            specilist_list.append({'cet_hospitals':cet_hospitals,'specilist':spc,'cet_doctors':cet_doctors,})
       
        blogs = Blog.objects.filter(is_active=True)
        # departments = Departments.objects.filter(hospital=hospital)
        
        print(hospitals) 
        param={'hospitals':hospitals_list,'doctors':doctor_list,'labs':labs_list,'pharmacys':pharmacys_list,'specilist_list':specilist_list,'blogs':blogs}
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
class SearchDoctorView(ListView):
    model = HospitalDoctors
    template_name = "front/doctor-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            doctors=HospitalDoctors.objects.filter( Q(is_virtual_available=True,is_active=True) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            doctors=HospitalDoctors.objects.filter(is_active=True).order_by(order_by)
            doctor_list = []
            for doctor in doctors:
                total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
                cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
                rating = 0
                for cmn in cmnss: 
                    rating = rating + cmn.rating
                if total_cmns == 0:
                    rating = rating /1
                else:    
                    rating = rating / total_cmns
                doctor_list.append({'doctor':doctor,'rating':rating,'total_cmns':total_cmns})
        return doctor_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchDoctorView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["doctors_number"]=HospitalDoctors.objects.filter(is_virtual_available=True,is_active=True).count()
        context["all_table_fields"]=HospitalDoctors._meta.get_fields()
        return context

class SearchOnlineHospitalView(ListView):
    model = HospitalDoctors
    template_name = "front/online-doctor-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            doctors=HospitalDoctors.objects.filter( Q(is_virtual_available=True,is_active=True) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            doctors=HospitalDoctors.objects.filter(is_virtual_available=True,is_active=True).order_by(order_by)
            doctor_list = []
            for doctor in doctors:
                total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
                cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
                rating = 0
                for cmn in cmnss: 
                    rating = rating + cmn.rating
                if total_cmns == 0:
                    rating = rating /1
                else:    
                    rating = rating / total_cmns
                doctor_list.append({'doctor':doctor,'rating':rating,'total_cmns':total_cmns})
        return doctor_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchOnlineHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["doctors_number"]=HospitalDoctors.objects.filter(is_virtual_available=True,is_active=True).count()
        context["all_table_fields"]=HospitalDoctors._meta.get_fields()
        return context

class SearchHomeVisitHospitalView(ListView):
    model = HospitalDoctors
    template_name = "front/homevisit-doctor-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            doctors=HospitalDoctors.objects.filter( Q(is_homevisit_available=True,is_active=True) ).order_by(order_by)
            #  (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            doctors=HospitalDoctors.objects.filter(is_homevisit_available=True,is_active=True).order_by(order_by)
            doctor_list = []
            for doctor in doctors:
                total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
                cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
                rating = 0
                for cmn in cmnss: 
                    rating = rating + cmn.rating
                if total_cmns == 0:
                    rating = rating /1
                else:    
                    rating = rating / total_cmns
                doctor_list.append({'doctor':doctor,'rating':rating,'total_cmns':total_cmns})
        return doctor_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchHomeVisitHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["doctors_number"]=HospitalDoctors.objects.filter(is_homevisit_available=True,is_active=True).count()
        context["all_table_fields"]=HospitalDoctors._meta.get_fields()
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
            
            total_cmns = RatingAndComments.objects.filter(HLP =lab.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =lab.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            lab_list.append({'lab':lab,'medias':medias,'services':services,'rating':rating,'total_cmns':total_cmns})
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
    model = Pharmacy
    template_name = "front/pharmacy-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            pharmacy=Pharmacy.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(pharmacy_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(address__contains=filter_val))).order_by(order_by)
        else:
            pharmacy=Pharmacy.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        
        pharma_list = []
        for pharma in pharmacy:
            medias = Medias.objects.filter(is_active=True,user=pharma.admin)
            total_cmns = RatingAndComments.objects.filter(HLP =pharma.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =pharma.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            pharma_list.append({'pharma':pharma,'medias':medias,'rating':rating,'total_cmns':total_cmns})       
        return pharma_list
     
    def get_context_data(self,**kwargs):
        context=super(SearchPharmacyView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["pharma_number"]=Pharmacy.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).count()
        context["all_table_fields"]=Pharmacy._meta.get_fields()
        return context

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
            total_cmns = RatingAndComments.objects.filter(HLP =hospital.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =hospital.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            hospital_media_list.append({'hospital':hospital,'medias':medias,'amount':amount,'rooms':rooms,'ambulances':ambulances,'room_max_price':room_max_price,'room_min_price':room_min_price,'rating':rating,'total_cmns':total_cmns})
        print(hospital_media_list)        
        return hospital_media_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["c_hospital"] = Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).count()
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

class SearcCathHospitalView(ListView):
    model = Hospitals
    template_name = "front/hospital-search.html"

    def get_queryset(self,*args, **kwargs):
        hid = self.kwargs['hid']
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            hospitals=Hospitals.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid) and (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            hospitals=Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid).order_by(order_by)
        
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
        context=super(SearcCathHospitalView,self).get_context_data(**kwargs)
        hid = self.kwargs['hid']
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["c_hospital"] = Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid).count()
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

class SearcCathDoctorView(ListView):
    model = HospitalDoctors
    template_name = "front/doctor-search.html"

    def get_queryset(self,*args, **kwargs):
        hid = self.kwargs['hid']
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            # doctors=HospitalDoctors.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid) and (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
            doctors=HospitalDoctors.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid,is_active=True).order_by(order_by)
        else:
            doctors=HospitalDoctors.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid,is_active=True).order_by(order_by)
        
        doctor_list = []
        for doctor in doctors:
            total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            doctor_list.append({'doctor':doctor,'rating':rating,'total_cmns':total_cmns})
        return doctor_list
    
    def get_context_data(self,**kwargs):
        context=super(SearcCathDoctorView,self).get_context_data(**kwargs)
        hid = self.kwargs['hid']
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["c_hospital"] = HospitalDoctors.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True,specialist=hid).count()
        context["all_table_fields"]=HospitalDoctors._meta.get_fields()
        return context

"""Details View Hospital"""
def UserVerified(request):
    if request.user.user_type == "4":
        if request.user.patients.is_verified == 0:
            return True
    else:
        return False 
        
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id'] 
        if request.user.is_authenticated:
            
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        hospital = 0
        try:
            if request.user.user_type == "1" or request.user.user_type == "2":
                hospital = get_object_or_404(Hospitals,id=hosital_id)
            else:
                hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        except:
            hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        # else:
        #     hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)  
        doctors = HospitalDoctors.objects.filter(is_active=True,hospital=hospital)
        A_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True,occupied=False).count()
        # O_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True,occupied=True).count()
        T_rooms = HospitalRooms.objects.filter(hospital=hospital,is_active=True).count()
        # T_room = A
        A_ambulances = AmbulanceDetails.objects.filter(hospital=hospital,is_active=True,occupied=False).count()
        T_ambulances = AmbulanceDetails.objects.filter(hospital=hospital,is_active=True).count()

        T_doctor = HospitalDoctors.objects.filter(hospital=hospital,is_active=True).count()

        T_patient = OrderBooking.objects.filter(HLP__hospitals=hospital).count()
        
        T_diseases = HospitalDisease.objects.filter(hospital=hospital).count()
        diseases = HospitalDisease.objects.filter(hospital=hospital)
        
        insurances = Insurances.objects.filter(hospital=hospital)
        cmns = RatingAndComments.objects.filter(HLP__hospitals =hospital)[0:5]

        total_cmns = RatingAndComments.objects.filter(HLP__hospitals =hospital).count()
        cmnss = RatingAndComments.objects.filter(HLP__hospitals =hospital)
        rating = 0 
        for cmn in cmnss:
            rating = rating + cmn.rating
       
        if total_cmns > 0: 
            rating = rating / total_cmns 

        #rating for bar 
        cmn_5 = RatingAndComments.objects.filter(HLP__hospitals =hospital,rating=5).count()
        cmn_5_per = 0
        if total_cmns > 0: 
            cmn_5_per = cmn_5 * 100 / total_cmns
        print(cmn_5_per)
        cmn_4 = RatingAndComments.objects.filter(HLP__hospitals =hospital,rating=4).count()
        cmn_4_per = 0
        if total_cmns > 0: 
            cmn_4_per = cmn_4 * 100 / total_cmns
        print(cmn_4_per)
        cmn_3 = RatingAndComments.objects.filter(HLP__hospitals =hospital,rating=3).count()
        cmn_3_per = 0
        if total_cmns > 0: 
            cmn_3_per = cmn_3 * 100 / total_cmns
        print(cmn_3_per)
        cmn_2 = RatingAndComments.objects.filter(HLP__hospitals =hospital,rating=2).count()
        cmn_2_per = 0
        if total_cmns > 0: 
            cmn_2_per = cmn_2 * 100 / total_cmns
        print(cmn_2_per)
        cmn_1 = RatingAndComments.objects.filter(HLP__hospitals =hospital,rating=1).count()
        cmn_1_per = 0
        if total_cmns > 0: 
            cmn_1_per = cmn_1 * 100 / total_cmns
        print(cmn_1_per)

        param = {'hospital':hospital,'medias':medias,'doctors':doctors,'A_rooms':A_rooms,'T_rooms':T_rooms,'A_ambulances':A_ambulances,'T_ambulances':T_ambulances,'cmns':cmns,'total_cmns':total_cmns,'rating':rating,'cmn_5':cmn_5,'cmn_1':cmn_1,'cmn_2':cmn_2,'cmn_3':cmn_3,'cmn_4':cmn_4,'cmn_1_per':cmn_1_per,'cmn_2_per':cmn_2_per,'cmn_3_per':cmn_3_per,'cmn_4_per':cmn_4_per,'cmn_5_per':cmn_5_per,'T_doctor':T_doctor,'T_patient':T_patient,'T_diseases':T_diseases,'diseases':diseases,'insurances':insurances}  

        return render(request,"front/new_hospital_details.html",param)

class HospitalComments(views.SuccessMessageMixin,View): 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self,request, *args, **kwargs): 
        patient = request.user
        HLP = request.POST.get('HLP')
        pagename = request.POST.get('pagename')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        hlp = get_object_or_404(CustomUser,id=HLP)
        print(patient,HLP,rating,comment)
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        ratingandcommect = RatingAndComments(patient=patient,HLP=hlp,rating=rating,comment=comment)
        ratingandcommect.save() 
        # messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!"
        if pagename == "hospital":
            return HttpResponseRedirect(reverse("hospital_details",kwargs={'id':hlp.hospitals.id}))
        elif pagename == "doctor":
            return HttpResponseRedirect(reverse("doctor_details",kwargs={'id':hlp.hospitaldoctors.id}))
        elif pagename == "lab":
            return HttpResponseRedirect(reverse("lab_details",kwargs={'id':hlp.labs.id}))
        elif pagename == "pharmacy":
            return HttpResponseRedirect(reverse("new_pharmacy_details",kwargs={'id':hlp.pharmacy.id}))

class CommentView(View):
    model = RatingAndComments
    template_name = "front/reviews.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            pharmacy=RatingAndComments.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(pharmacy_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(address__contains=filter_val))).order_by(order_by)
        else:
            pharmacy=RatingAndComments.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        
        pharma_list = []
        for pharma in pharmacy:
            medias = Medias.objects.filter(user=pharma.admin)
            pharma_list.append({'pharma':pharma,'medias':medias})       
        return pharma_list

class DoctorsBookAppoinmentViews(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        # hositaldcotorid_id=kwargs['did']
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        # hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        doctor = get_object_or_404(HospitalDoctors,is_active=True,id=hosital_id)
        if request.user.user_type == "4":
            showdate = datetime.now(tz=IST).date()
            showtime = datetime.now(tz=IST).time()
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor).filter(showdate__gte=showdate)
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns        

            token =False
            param = {'doctor':doctor,'doctorschedules':doctorschedules,'token':token,'someones':forsome,'rating':rating,'total_cmns':total_cmns}  
            return render(request,"front/booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))  
     
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['id'] 
        doctor = get_object_or_404(HospitalDoctors,is_active=True,id=doc_id)
        showdate = datetime.now(tz=IST).date()
        showtime = datetime.now(tz=IST).time()
        print(date,showdate)
        if date == showdate:
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date).filter(showtime__gte=showtime)
        else:
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        if request.user.user_type == "4":
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            token = True
            param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token,'someones':forsome,'rating':rating,'total_cmns':total_cmns}  
            return render(request,"front/booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("bookappoinment",kwargs={'id':doctor.hospital.id,'did':doctor.id}))

class DoctorDetailsViews(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        doctor_id=kwargs['id']
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        showdate = datetime.now(tz=IST).date()
        showtime = datetime.now(tz=IST).time()
        doctor = get_object_or_404(HospitalDoctors,is_active=True,id=doctor_id)
        # if request.user.user_type == "4":
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,is_active=True)

        forsome = ""
        if request.user.user_type == "4":
            forsome = ForSome.objects.filter(patient = request.user.patients)
        cmns = RatingAndComments.objects.filter(HLP =doctor.admin)[0:5]
    
        total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
        cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
        rating = 0 
        for cmn in cmnss:
            rating = rating + cmn.rating

    
        if total_cmns > 0: 
            rating = rating / total_cmns 

        #rating for bar 
        cmn_5 = RatingAndComments.objects.filter(HLP =doctor.admin,rating=5).count()
        cmn_5_per = 0
        if total_cmns > 0: 
            cmn_5_per = cmn_5 * 100 / total_cmns
        print(cmn_5_per)
        cmn_4 = RatingAndComments.objects.filter(HLP =doctor.admin,rating=4).count()
        cmn_4_per = 0
        if total_cmns > 0: 
            cmn_4_per = cmn_4 * 100 / total_cmns
        print(cmn_4_per)
        cmn_3 = RatingAndComments.objects.filter(HLP =doctor.admin,rating=3).count()
        cmn_3_per = 0
        if total_cmns > 0: 
            cmn_3_per = cmn_3 * 100 / total_cmns
        print(cmn_3_per)
        cmn_2 = RatingAndComments.objects.filter(HLP =doctor.admin,rating=2).count()
        cmn_2_per = 0
        if total_cmns > 0: 
            cmn_2_per = cmn_2 * 100 / total_cmns
        print(cmn_2_per)
        cmn_1 = RatingAndComments.objects.filter(HLP =doctor.admin,rating=1).count()
        cmn_1_per = 0
        if total_cmns > 0: 
            cmn_1_per = cmn_1 * 100 / total_cmns
        print(cmn_1_per)
        token =False
        param = {'doctor':doctor,'doctorschedules':doctorschedules,'token':token,'someones':forsome,'rating':rating,'total_cmns':total_cmns,'cmns':cmns,'total_cmns':total_cmns,'rating':rating,'cmn_5':cmn_5,'cmn_1':cmn_1,'cmn_2':cmn_2,'cmn_3':cmn_3,'cmn_4':cmn_4,'cmn_1_per':cmn_1_per,'cmn_2_per':cmn_2_per,'cmn_3_per':cmn_3_per,'cmn_4_per':cmn_4_per,'cmn_5_per':cmn_5_per,}  
        return render(request,"front/booking.html",param)
        # else:
        #     messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
        #     return HttpResponseRedirect(reverse("front_home"))  
     
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['did'] 
        doctor = get_object_or_404(HospitalDoctors,is_active=True,id=doc_id)
        showdate = datetime.now(tz=IST).date()
        showtime = datetime.now(tz=IST).time()
        print(showdate,date)
        if str(date) == str(showdate):
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date).filter(timeslot__schedule__gte=showtime)
        else:
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        if request.user.user_type == "4":
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            total_cmns = RatingAndComments.objects.filter(HLP =doctor.admin).count()
            cmnss = RatingAndComments.objects.filter(HLP =doctor.admin)
            rating = 0
            for cmn in cmnss: 
                rating = rating + cmn.rating
            if total_cmns == 0:
                rating = rating /1
            else:    
                rating = rating / total_cmns
            token = True
            param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token,'someones':forsome}  
            return render(request,"front/booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("bookappoinment",kwargs={'id':doctor.id}))

"""Pharmacy Details"""
class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        pharmacy_id=kwargs['id']
        # if request.user.user_type == "4": 
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        pharmacy = get_object_or_404(Pharmacy,is_verified=True,is_deactive=False,id=pharmacy_id)
        medias = Medias.objects.filter(is_active=True,user=pharmacy.admin)  
        cmns = RatingAndComments.objects.filter(HLP =pharmacy.admin)[0:5]
    
        total_cmns = RatingAndComments.objects.filter(HLP =pharmacy.admin).count()
        cmnss = RatingAndComments.objects.filter(HLP =pharmacy.admin)
        rating = 0 
        for cmn in cmnss:
            rating = rating + cmn.rating        
        if total_cmns > 0: 
            rating = rating / total_cmns 

        #rating for bar 
        cmn_5 = RatingAndComments.objects.filter(HLP =pharmacy.admin,rating=5).count()
        cmn_5_per = 0
        if total_cmns > 0: 
            cmn_5_per = cmn_5 * 100 / total_cmns
        print(cmn_5_per)
        cmn_4 = RatingAndComments.objects.filter(HLP =pharmacy.admin,rating=4).count()
        cmn_4_per = 0
        if total_cmns > 0: 
            cmn_4_per = cmn_4 * 100 / total_cmns
        print(cmn_4_per)
        cmn_3 = RatingAndComments.objects.filter(HLP =pharmacy.admin,rating=3).count()
        cmn_3_per = 0
        if total_cmns > 0: 
            cmn_3_per = cmn_3 * 100 / total_cmns
        print(cmn_3_per)
        cmn_2 = RatingAndComments.objects.filter(HLP =pharmacy.admin,rating=2).count()
        cmn_2_per = 0
        if total_cmns > 0: 
            cmn_2_per = cmn_2 * 100 / total_cmns
        print(cmn_2_per)
        cmn_1 = RatingAndComments.objects.filter(HLP =pharmacy.admin,rating=1).count()
        cmn_1_per = 0
        if total_cmns > 0: 
            cmn_1_per = cmn_1 * 100 / total_cmns
        print(cmn_1_per)
    
        param = {'pharmacy':pharmacy,'medias':medias,'total_cmns':total_cmns,'cmns':cmns,'rating':rating,'cmn_5':cmn_5,'cmn_1':cmn_1,'cmn_2':cmn_2,'cmn_3':cmn_3,'cmn_4':cmn_4,'cmn_1_per':cmn_1_per,'cmn_2_per':cmn_2_per,'cmn_3_per':cmn_3_per,'cmn_4_per':cmn_4_per,'cmn_5_per':cmn_5_per,}  
        return render(request,"front/pharmacy_details.html",param)
        # else:
        #     messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
        #     return HttpResponseRedirect(reverse("front_home"))   

"""Lab Details"""
class LabDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id'] 
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update")) 
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        medias = Medias.objects.filter(is_active=True,user=lab.admin)  
        services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True)
        total_services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True).count()

        cmns = RatingAndComments.objects.filter(HLP =lab.admin)[0:5]
        
        total_cmns = RatingAndComments.objects.filter(HLP =lab.admin).count()
        cmnss = RatingAndComments.objects.filter(HLP =lab.admin)
        rating = 0 
        for cmn in cmnss:
            rating = rating + cmn.rating

       
        if total_cmns > 0: 
            rating = rating / total_cmns 

        #rating for bar 
        cmn_5 = RatingAndComments.objects.filter(HLP =lab.admin,rating=5).count()
        cmn_5_per = 0
        if total_cmns > 0: 
            cmn_5_per = cmn_5 * 100 / total_cmns
        print(cmn_5_per)
        cmn_4 = RatingAndComments.objects.filter(HLP =lab.admin,rating=4).count()
        cmn_4_per = 0
        if total_cmns > 0: 
            cmn_4_per = cmn_4 * 100 / total_cmns
        print(cmn_4_per)
        cmn_3 = RatingAndComments.objects.filter(HLP =lab.admin,rating=3).count()
        cmn_3_per = 0
        if total_cmns > 0: 
            cmn_3_per = cmn_3 * 100 / total_cmns
        print(cmn_3_per)
        cmn_2 = RatingAndComments.objects.filter(HLP =lab.admin,rating=2).count()
        cmn_2_per = 0
        if total_cmns > 0: 
            cmn_2_per = cmn_2 * 100 / total_cmns
        print(cmn_2_per)
        cmn_1 = RatingAndComments.objects.filter(HLP =lab.admin,rating=1).count()
        cmn_1_per = 0
        if total_cmns > 0: 
            cmn_1_per = cmn_1 * 100 / total_cmns
        print(cmn_1_per)
      
        param = {'lab':lab,'medias':medias,'services':services,'total_services':total_services,'total_cmns':total_cmns,'cmns':cmns,'rating':rating,'cmn_5':cmn_5,'cmn_1':cmn_1,'cmn_2':cmn_2,'cmn_3':cmn_3,'cmn_4':cmn_4,'cmn_1_per':cmn_1_per,'cmn_2_per':cmn_2_per,'cmn_3_per':cmn_3_per,'cmn_4_per':cmn_4_per,'cmn_5_per':cmn_5_per,}  
        return render(request,"front/lab_details.html",param)

class LabAppoinmentViews(View):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id'] 
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))  
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        medias = Medias.objects.filter(is_active=True,user=lab.admin)  
        services = ServiceAndCharges.objects.filter(user__labs = lab,is_active = True) 
        if request.user.user_type == "4":
            doctorschedules = LabSchedule.objects.filter(lab=lab)
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            token =False 
            param = {'lab':lab,'medias':medias,'services':services,'doctorschedules':doctorschedules,'token':token,'someones':forsome}  
            return render(request,"front/Lab-booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))

    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        lab_id=kwargs['id']
        if request.user.user_type == "4":
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
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))

"""PDF generator"""
def pdfgenerator(request,id):
    #File/PDF generate code---Create ByteStream buffer
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    #create a text object
    textobj = c.beginText()
    textobj.setTextOrigin(inch, inch)
    textobj.setFont("Helvetica",14)
    # Add lines of text
    lines = [
        "This is line one",
        "This is line two",
        "This is line three",
    ] 
    #Loop 
    for line in lines:
        textobj.textLine(line)
    #finish up
    c.drawText(textobj)
    c.showPage()
    c.save()
    buf.seek(0)
    # response = HttpResponse(content_type='application/pdf') 
    # response['Content-Disposition'] = 'attachment; filename="1.pdf"'
    # return response
    return FileResponse(buf,as_attachment=True,filename="invoice.pdf")

"""Appointment booking"""

class BookAnAppointmentViews(views.SuccessMessageMixin,View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self,request, *args, **kwargs):
        # try:
        if request.user.user_type == "4" and request.user.patients.is_verified == True:
            doctorid = request.POST.get('doctor_id')       
            timeslot = request.POST.get('timeslot')
            serviceid_list = request.POST.getlist('serviceid[]')
            someone = request.POST.get('someone')       
            date = request.POST.get('date')       
            where = request.POST.get('orderwhere')
            booking_type = request.POST.get('booking_type')
            add_note = request.POST.get('add_note')
            prescription = request.FILES.get('prescription')
            now = datetime.now()
            now5 = now + timedelta(minutes=5)
            if request.user.is_authenticated:
                a = UserVerified(request)
                if a:
                    messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                    return HttpResponseRedirect(reverse("patient_update")) 
            with transaction.atomic():
                booking = OrderBooking(patient = request.user,applied_date=date,is_applied=True,is_active=True,status="BOOKED")
                booking.reject_within_5__lt = now            
            booking.reject_within_5 = now5
            booking.payment_status="INPROCESS"
            if someone:
                forsome = get_object_or_404(ForSome,id=someone)
                booking.for_whom=forsome
            if where == "hospital":
                hospitalstaffdoctor = get_object_or_404(HospitalDoctors,id=doctorid)
                doctorschedule = get_object_or_404(DoctorSchedule,id=timeslot,doctor=hospitalstaffdoctor)
                doctorschedule.is_booked =True
                doctorschedule.save()
                booking.applied_time=doctorschedule.timeslot.schedule
                booking.hospitalstaffdoctor=hospitalstaffdoctor
                try:
                # if hospitalstaffdoctor.hospital.admin.user_type == "2":
                    booking.HLP=hospitalstaffdoctor.hospital.admin
                    booking.booking_for="H"
                except:               
                    booking.HLP=hospitalstaffdoctor.admin
                    booking.booking_for="D"
                booking.booking_type=booking_type           
                if booking_type == "EMERGENCY": 
                    booking.amount=hospitalstaffdoctor.emergency_charges
                if booking_type == "OPD":
                    booking.amount=hospitalstaffdoctor.opd_charges
                if booking_type == "ONLINE":
                    booking.amount=hospitalstaffdoctor.online_charges
                if booking_type == "HOMEVISIT":
                    booking.amount=hospitalstaffdoctor.home_charges           
                  
            if where == "lab": 
                booking.booking_for="L"
                lab = get_object_or_404(Labs,id=doctorid)
                labschedule = get_object_or_404(LabSchedule,id=timeslot,lab=lab)
                labschedule.is_booked =True
                labschedule.save()
                booking.applied_time=labschedule.timeslot.schedule
                booking.HLP=lab.admin
                booking.booking_type=booking_type
                total = 0
                booking.save()
                for service in serviceid_list:
                    ser = get_object_or_404(ServiceAndCharges,id=service)
                    labtest = NewLabTest(booking=booking,service=ser)
                    labtest.save()       
                    total = total + ser.service_charge
                if booking_type == "AT-HOME":
                    homevisticharge =get_object_or_404(HomeVisitCharges,lab = lab)
                    booking.homevisitcharges = homevisticharge.charges
                    total = total + homevisticharge.charges
                booking.amount = total 

            if where == "pharma":
                if prescription:
                    booking.prescription = prescription
                pharmacy =get_object_or_404(Pharmacy,id=doctorid)
                booking.HLP=pharmacy.admin
                booking.booking_for="P"
                booking.booking_type=booking_type
                booking.applied_time=timeslot
                booking.is_amount_paid = False
                booking.add_note = add_note
            # booking.invoice = pdfgenerator()
            # print(booking.invoice)
            booking.save()
            tc = 0
            try:
                tc = Temp.objects.filter(user=request.user).count()
            except:
                tc = 0
            print("tc check below")
            print(tc)
            if tc > 0:
                temp = Temp.objects.filter(user=request.user)
                for tmp in temp:
                    tmp.delete()
            temp =  Temp(user=request.user,order_id=booking.order_id)
            temp.save()            
            mobile= request.user.phone
            key = send_otp(mobile)
            if key: 
                obj = phoneOPTforoders(order_id=booking,user=request.user,otp=key)
                obj.save()
                notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.HLP,booking=booking)
                notification.save()
                    # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                    # res = conn.getresponse()
                    # data = res.read()
                    # data=data.decode("utf-8")
                    # data=ast.literal_eval(data)
                    # print(data)
                # current_site=get_current_site(request) #fetch domain    
                # email_subject='Active your Account',
                # message=render_to_string('accounts/order.html',
                # {
                #     'Order_id':booking.id,
                #     'domain':current_site.domain,

                # } #convert Link into string/message
                # )
                # print(message)
                # email_message=EmailMessage(
                #     email_subject, 
                #     message,
                #     settings.EMAIL_HOST_USER,
                #     [booking.patient.email]
                # )#compose email
                # email_message.attach(attach.name, attach.read(), attach.content_type)
                # print(email_message)
                # email_message.send() #send Email
                # messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")
            if booking.booking_for == "P":
                return render(request,"front/amount_confirmation.html")            
            else:            
                return HttpResponseRedirect(reverse("checkout"))  
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))
            # return HttpResponseRedirect(reverse("bookappoinment",kwargs={'id':booking.hospitalstaffdoctor.id,'did':hospitalstaffdoctor.id}))

        #     # return JsonResponse({'message' : 'success','status': True,'Booking_id':booking.id,"otp":key})
        # else:
        #     return JsonResponse({'message' : 'Error','status': False})

class InvoiceViews(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        id=kwargs['id'] 
        booking = get_object_or_404(OrderBooking,id=id)          
        book_for=booking.booking_for
        param = {}
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))
        if book_for == "H" or book_for == "D":
            param ={'booking':booking} 
        if book_for == "L":
            services = NewLabTest.objects.filter(booking=booking)
            param ={'booking':booking,'services':services}
        if book_for == "P":
            param ={'booking':booking}
        return render(request,"front/invoice-view.html",param)
     
"""Review delete for all"""
def deleteReviews(request,id):
    try:
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))
        if request.user.user_type == "4" or request.user.is_superuser:
            rev = get_object_or_404(RatingAndComments,id=id,patient=request.user)
            rev.delete()
            messages.add_message(request,messages.SUCCESS,"Deleted Successfully")
            return HttpResponseRedirect(reverse("patine_reviews"))
        elif request.user.user_type == "1":
            rev = get_object_or_404(RatingAndComments,id=id)
            rev.delete()
            messages.add_message(request,messages.SUCCESS,"Deleted Successfully")
            return HttpResponseRedirect(reverse("admin_reviews"))
        else:
            messages.add_message(request,messages.ERROR,"YOu are not Autosried")
            return HttpResponseRedirect(reverse("front_home"))

    except Exception as e:
        messages.add_message(request,messages.ERROR,"Somethingwent wrong")
        return HttpResponseRedirect(reverse("front_home"))
    

"""Reviews list and edit delete """

class BLoodDonorList(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))
        last_three_month = datetime.today() - timedelta(days=90)
        patients = Patients.objects.filter(admin__is_active=True,blood_donation =True,blood_docation_date__lte = last_three_month)
        print(patients)
        return render(request,"front/blood-donor-search.html",{'patients':patients})
    
class BloodRequestView(View):   
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))
        last_three_month = datetime.today() - timedelta(days=90)
        patients = Patients.objects.filter(admin__is_active=True,blood_donation =True,blood_docation_date__lte = last_three_month)
        print(patients)
        return render(request,"front/blood-donor-search.html",{'patients':patients})
    
    def post(self, request, *args, **kwargs):
        reqestpersoned = request.user        
        id = request.POST.get('forpersoned')
        print(id)
        print(reqestpersoned)
        try:
            forpersoned = get_object_or_404(CustomUser,id=id) 
            donorrequest = DonorRequest(reqestpersoned=reqestpersoned,forpersoned=forpersoned)
            donorrequest.save()
            return HttpResponseRedirect(reverse("successfullpage",kwargs={'id':donorrequest.id}))
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Somethingwent wrong")
            return HttpResponseRedirect(reverse("search_blood_donor")) 

class DonorRequestDone(DetailView): 
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id'] 
        if request.user.is_authenticated:
            a = UserVerified(request)
            if a:
                messages.add_message(request,messages.ERROR,"PLEASE COMPLETE YOUR PROFILE FIRST")
                return HttpResponseRedirect(reverse("patient_update"))
        donorrequest = get_object_or_404(DonorRequest,id=lab_id)
        donorrequest.is_active=True
        donorrequest.save()
        return render(request,"front/donor-success.html",{"donorrequest":donorrequest})


