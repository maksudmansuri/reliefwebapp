from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View,ListView

from django.contrib import messages
from django.db.models import Q
from accounts.models import Hospitals, Labs, Pharmacy
from hospital.models import HospitalMedias
from patient.views import HospitalListViews

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

class SearchHospitalView(ListView):
    paginate_by = 10
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
            medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)           
            hospital_media_list.append({'hospital':hospital,'medias':medias})
        print(hospital_media_list)        
        return hospital_media_list
   
    def get_context_data(self,**kwargs):
        context=super(HospitalListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context
    