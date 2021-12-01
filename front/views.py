import json
from django.contrib.messages import views
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.views.generic import View,ListView,DetailView

from django.contrib import messages
from django.db.models import Q
from accounts.models import AdminHOD, Hospitals, Labs, Pharmacy, Specailist
from hospital.models import Blog, DoctorSchedule, HospitalMedias, HospitalStaffDoctors, ServiceAndCharges
from django.http import JsonResponse

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
    paginate_by = 5
    queryset = Blog.objects.filter(is_active=True)

class BlogDetailsView(DetailView):
    model = Blog
    template_name = "front/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_list"] = Blog.objects.filter(is_active = True) 
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
            hospital_media_list.append({'hospital':hospital,'medias':medias,'amount':amount})
        print(hospital_media_list)        
        return hospital_media_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id'] 
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)  
        doctors = HospitalStaffDoctors.objects.filter(is_active=True,hospital=hospital)
        amount = ServiceAndCharges.objects.get(user=hospital.admin,service_name = "OPD")
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
        # hospitalstaffdoctor_list = []
        # for hospitalstaffdoctor in doctors:
        #     hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        #     opd_time = []
        #     for dcsh in hospitalstaffdoctorschedual:
        #         if dcsh.work == "OPD":
        #             start_time = dcsh.start_time
        #             end_time = dcsh.end_time
        #         opd_time.append({'start_time':start_time,'end_time':end_time})
        #     hospitalstaffdoctor_list.append({'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual})
        param = {'hospital':hospital,'hospitalservice':hospitalservice,'medias':medias,'amount':amount,'doctors':doctors}  
        return render(request,"front/new_hospital_details.html",param)

class DoctorsBookAppoinmentViews(View):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=hositaldcotorid_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,hospital=hospital)      
        token =False
        param = {'hospital':hospital,'doctor':doctor,'doctorschedules':doctorschedules,'token':token}  
        return render(request,"front/booking.html",param)
    
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['did'] 
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=doc_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        print(date,doctor,doctorschedules)
        token = True
        param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token}  
        return render(request,"front/booking.html",param)

