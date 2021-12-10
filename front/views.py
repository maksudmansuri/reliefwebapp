import json
from django.contrib.auth.decorators import login_required
from django.contrib.messages import views
from django.core import paginator
from django.core.files.storage import FileSystemStorage
from django.db.models.base import Model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View,ListView,DetailView

from django.contrib import messages
from django.db.models import Q
from chat.models import Notification
from accounts.models import AdminHOD, Hospitals, Labs, Patients, Pharmacy, Specailist
from accounts.views import send_otp
from hospital.models import AmbulanceDetails, Blog, DoctorSchedule, HospitalMedias, HospitalRooms, HospitalStaffDoctors, ServiceAndCharges
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime,timedelta
from django.db.models import Avg, Max, Min, Sum
from lab.models import HomeVisitCharges, LabSchedule, Medias
import patient


from patient.models import ForSome, NewLabTest, OrderBooking, Temp, phoneOPTforoders
# Create your views here.
  
class FrontView(View):
    def get(self, request, *args, **kwargs):
        
        hospitals=Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        labs=Labs.objects.filter(admin__is_active=True,is_verified = True)
        pharmacys=Pharmacy.objects.filter(admin__is_active=True,is_verified = True)
        specilist = Specailist.objects.all()
        specilist_list = [] 
        for spc in specilist:
            cet_hospitals = Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False,specialist = spc).count()
            specilist_list.append({'cet_hospitals':cet_hospitals,'specilist':spc})
        blogs = Blog.objects.filter(is_active=True)
        # departments = Departments.objects.filter(hospital=hospital)
        print(hospitals) 
        param={'hospitals':hospitals,'labs':labs,'pharmacys':pharmacys,'specilist_list':specilist_list,'blogs':blogs}
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
            pharma_list.append({'pharma':pharma,'medias':medias})       
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
            hospital_media_list.append({'hospital':hospital,'medias':medias,'amount':amount,'rooms':rooms,'ambulances':ambulances,'room_max_price':room_max_price,'room_min_price':room_min_price})
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
        if request.user.user_type == "4":
            doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,hospital=hospital)
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            token =False
            param = {'hospital':hospital,'doctor':doctor,'doctorschedules':doctorschedules,'token':token,'someones':forsome}  
            return render(request,"front/booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))  
     
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['did'] 
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=doc_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        if request.user.user_type == "4":
            forsome = ForSome.objects.filter(patient = request.user.patients) 
            print(date,doctor,doctorschedules)
            token = True
            param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token,'someones':forsome}  
            return render(request,"front/booking.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))

"""Pharmacy Details"""
class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        pharmacy_id=kwargs['id']
        if request.user.user_type == "4": 
            pharmacy = get_object_or_404(Pharmacy,is_verified=True,is_deactive=False,id=pharmacy_id)
            medias = Medias.objects.filter(is_active=True,user=pharmacy.admin)  
       
            param = {'pharmacy':pharmacy,'medias':medias}  
            return render(request,"front/pharmacy_details.html",param)
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))   

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

"""Appointment booking"""

class BookAnAppointmentViews(views.SuccessMessageMixin,View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self,request, *args, **kwargs):
        # try:
        if request.user.user_type == "4":
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
            
            with transaction.atomic():
                booking = OrderBooking(patient = request.user,applied_date=date,is_applied=True,is_active=True,status="BOOKED")
                booking.reject_within_5__lt = now            
            booking.reject_within_5 = now5
            booking.payment_status="INPROCESS"
            if someone:
                forsome = get_object_or_404(ForSome,id=someone)
                booking.for_whom=forsome
            if where == "hospital":
                hospitalstaffdoctor = get_object_or_404(HospitalStaffDoctors,id=doctorid)
                doctorschedule = get_object_or_404(DoctorSchedule,id=timeslot,doctor=hospitalstaffdoctor)
                doctorschedule.is_booked =True
                doctorschedule.save()
                booking.applied_time=doctorschedule.timeslot.schedule
                booking.hospitalstaffdoctor=hospitalstaffdoctor
                booking.HLP=hospitalstaffdoctor.hospital.admin
                booking.booking_for="H"
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
                    fs=FileSystemStorage()
                    filename1=fs.save(prescription.name,prescription)
                    prescription_url=fs.url(filename1)
                    booking.prescription = prescription_url
                pharmacy =get_object_or_404(Pharmacy,id=doctorid)
                booking.HLP=pharmacy.admin
                booking.booking_for="P"
                booking.booking_type=booking_type
                booking.applied_time=timeslot
                booking.is_amount_paid = False
                booking.add_note = add_note
            booking.save()
            tc = 0
            try:
                tc = Temp.objects.filter(user=request.user).count()
            except:
                tc = 0
            print("tc check below")
            print(tc)
            if tc > 0:
                temp = Temp.objects.get(user=request.user)
                temp.delete()
            temp =  Temp(user=request.user,order_id=booking.order_id)
            temp.save() 
            
            print(booking.reject_within_5__lt)
            print(booking.reject_within_5)
    
            print("booking saved")
            mobile= request.user.phone
            key = send_otp(mobile)
            print(key)
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
            if booking.booking_for == "P":
                return render(request,"front/amount_confirmation.html")            
            else:            
                return HttpResponseRedirect(reverse("checkout"))  
        else:
            messages.add_message(request,messages.ERROR,"Your Account is not authorized to book...!")
            return HttpResponseRedirect(reverse("front_home"))  
        #     # return JsonResponse({'message' : 'success','status': True,'Booking_id':booking.id,"otp":key})
        # else:
        #     return JsonResponse({'message' : 'Error','status': False})

class InvoiceViews(View):
    def get(self, request, *args, **kwargs):
        id=kwargs['id'] 
        booking = get_object_or_404(OrderBooking,id=id)          
        book_for=booking.booking_for
        if book_for == "H":
            param ={'booking':booking} 
        if book_for == "L":
            services = NewLabTest.objects.filter(booking=booking)
            param ={'booking':booking,'services':services}
        if book_for == "P":
            param ={'booking':booking}
        return render(request,"front/invoice-view.html",param)
     

class BLoodDonorList(View):
    def get(self, request, *args, **kwargs):
        last_three_month = datetime.today() - timedelta(days=90)
        patients = Patients.objects.filter(admin__is_active=True,blood_donation =True,blood_docation_date__lte = last_three_month)
        print(patients)
        return render(request,"front/blood-donor-search.html",{'patients':patients})