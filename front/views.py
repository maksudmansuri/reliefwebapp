from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import View,ListView,DetailView

from django.contrib import messages
from django.db.models import Q
from accounts.models import Hospitals, Labs, Pharmacy, Specailist
from hospital.models import Blog, HospitalMedias

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
    paginate_by = 5
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
        context=super(SearchHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        context["hospital_media_list"]=Hospitals._meta.get_fields()
        return context
    