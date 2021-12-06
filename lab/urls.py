from django.urls import path
from django.urls.conf import re_path
from django.views.generic.base import View
from .import views

urlpatterns = [ 
    path('',views.LabDashboardViews.as_view(),name="lab_home"),
    path('lab_update',views.LabUpdateViews.as_view(),name="lab_update"),
 
    #view-schedule
    path('manage_labschedule',views.LabScheduleCreateView.as_view(),name="manage_labschedule"),
    path('delete_labschedule/<id>',views.deleteTimeSlot,name="delete_labschedule"), 

    path('add_lab_homevisitupdate',views.HomeServicesUpdateViews,name="add_lab_homevisitupdate"),
    path('add_lab_homevisit',views.HomeServicesViews,name="add_lab_homevisit"),
    path('add_lab_services',views.ServicesViews.as_view(),name="add_lab_services"),
    path('update_lab_services',views.UpdateServicesViews,name="update_lab_services"),
    path('delete_lab_services/<id>',views.deleteServicesViews,name="delete_lab_services"),
     
    path('view_lab_appointment',views.ViewAppointmentViews.as_view(),name="view_lab_appointment"),
    path('delete_lab_appointment/<id>',views.dateleLabAppointment,name="delete_lab_appointment"),

    #add media delete
    path('manage_main_gallery',views.ManageMainGalleryView.as_view(),name="manage_main_gallery"),
    path('delete_main_gallery',views.deleteMainGallery,name="delete_main_gallery"),

    path('updload_lab_report/<id>',views.UploadReportViews,name="updload_lab_report"),


    re_path('verifylabtestbooking',views.verifylabtestbooking,name="verifylabtestbooking"),
    

 
]