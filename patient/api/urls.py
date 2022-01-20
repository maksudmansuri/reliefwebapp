from patient.api import views
from django.urls import path,include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'specialist', views.specialistViewSets)
# router.register(r'delivery-cost', views.DeliveryCostViewSet)
urlpatterns = [
    path('', include((router.urls, 'relief.patient.api'))),

    #New API By page
    path('homescreen', views.HomeScreenView.as_view(),name='homescreen'),

    #Hospital's APIs     
    re_path('hospitalslist/', views.ApiHospitalListAndDetailsView.as_view(),name='hospitalslist'),
    path('hospitalslist/<id>', views.ApiHospitalListAndDetailsView.as_view(),name='hospitalsdetials'),
    #Doctorhosptial Apis
    # path('hospitaldoctordetail/<id>/<did>', views.HospitalDoctorDetailsView.as_view(),name='hospitaldoctordetail'),
    #Online Doctor Apis
    path('onlinedoctors',views.APIOnlineDoctorListView.as_view(),name='onlinedoctorlist'),
    path('onlinedoctors/<id>',views.APIOnlineDoctorListView.as_view(),name='onlinedoctordetail'),
    #Doctor Apis
    path('doctors',views.HospitalDoctorDetailsView.as_view(),name='doctorlist'),
    path('doctors/<id>',views.HospitalDoctorDetailsView.as_view(),name='doctordetail'),
    #HomeDoctor Apis
    path('homevisitdoctors',views.APIHomevisitDoctorListView.as_view(),name='homevisitdoctorlist'),
    path('homevisitdoctors/<id>',views.APIHomevisitDoctorListView.as_view(),name='homevisitdetail'),
    # path('doctorschedules/<id>/<did>/<sid>', views.HospitalDoctorDetailsView.as_view(),name='hospitaldoctordetail'),

    # Lab's APIs
    path('labs', views.ApiLabsListAndDetailsView.as_view(),name='labslist'),
    path('labs/<id>', views.ApiLabsListAndDetailsView.as_view(),name='labsdetials'),
  
    # Pharmacy's APIs
    path('pharmacy', views.ApiPharmacyListAndDetailsView.as_view(),name='pharmacylist'),
    path('pharmacy/<id>', views.ApiPharmacyListAndDetailsView.as_view(),name='pharmacydetials'),

    # List Of AppointmentBooked
    path('appointmentlist', views.AppointmentListView.as_view(),name='appointmentlist'),
    path('appointmentdetail/<id>', views.AppointmentListView.as_view(),name='appointmentdetail'),

]
