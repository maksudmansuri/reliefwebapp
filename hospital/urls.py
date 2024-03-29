from django.urls import path
from django.urls.conf import re_path
from .import views
from patient import views as patientView
from front import views as frontView

urlpatterns = [   
    # path('',views.indexView,name="hospital_home"),
    path('',views.hospitaldDashboardViews.as_view(),name="hospital_dashboard"),
    path('hospital_update',views.hospitalUpdateViews.as_view(),name="hospital_update"),
    path('hospital_profile',frontView.HospitalDetailsViews.as_view(),name="hospital_profile"),

    #Order Booking for hospital ,Lab ,pharmacy, 
    #Hospital
    path('accept_apt/<id>',views.AcceptAPT,name="accept_apt"),
    path('accept_otp/<id>',views.AcceptOTP,name="accept_otp"),
    path('reject_apt/<id>',views.RejectedAPT,name="reject_apt"),

    #review list
    path('hospitalreviews/',views.HospitalReviewsListView.as_view(),name="hospitalreviews"),
    
    
    # for treatment tab menu Treatment includes Diseas , Medicine(with time) , Reports , Follow ups dates , Exercise 
 

    path('manage_relief_patient',views.manageReliefPatientViews.as_view(),name="manage_relief_patient"),
    path('relief_patient_profile/<id>',views.ReliefPatientViewsProfile.as_view(),name="relief_patient_profile"),
    path('relief_patient_files/<id>',views.ReliefPatientViewsFiles,name="relief_patient_files"),
    path('manage_treatment/<id>',views.manageTreatmentViews.as_view(),name="manage_treatment"),
    path('delete__relief_hospital_patient/<id>',views.deleteReliefHospitalPatient,name="delete__relief_hospital_patient"),


    #Staff list ,add ,update ,delete
    path('manage_staff',views.manageStaffView.as_view(),name="manage_staff"),
    path('update_staff',views.updateStaff,name="update_staff"),
    
    #patient list ,add ,update ,delete
    path('manage_patient',views.managePatientView.as_view(),name="manage_patient"),
    path('update_patient',views.updatePatientView,name="update_patient"),
    path('delete__hospital_patient/<id>',views.deleteHospitalPatient,name="delete__hospital_patient"),
    
    # Appointment Update Delete treatment
    path('manage_appointment',views.manageAppointmentView.as_view(),name="manage_appointment"),
    # path('update_appointment',views.updateAppointment,name="update_appointment"),
    path('delete_appointment/<id>',views.dateleAppointment,name="delete_appointment"),
    
    #deaprtment manage add update delete 
    path('manage_department',views.manageDepartmentclassView.as_view(),name="manage_department"),
    path('update_department',views.updateDepartment,name="update_department"),
 
    #deaprtment manage add update delete 
    path('manage_room',views.manageRoomclassView.as_view(),name="manage_room"),
    path('update_room/<id>',views.updateRoom,name="update_room"),
    
    #Ambulance manage add update delete 
    path('manage_ambulance',views.manageAmbulanceclassView.as_view(),name="manage_ambulance"), 
    path('update_ambulance',views.updateAmbulance,name="update_ambulance"),
    path('delete_ambulance/<id>',views.deleteAmbulance,name="delete_ambulance"),


    # Add Doctor Update Doctor
    path('manage_doctor',views.manageDoctorView.as_view(),name="manage_doctor"),
    path('update_doctor',views.updateDoctor,name="update_doctor"),

    # Price Doctor Update Doctor
    path('manage_price',views.managePricesView.as_view(),name="manage_price"),
    path('update_service_price',views.updateServicePrice,name="update_service_price"),
    path('delete_service_price/<id>',views.deleteServicePrice,name="delete_service_price"),

     #List  Add Update Doctor schedual  Doctor
    path('manage_doctorschedule/<id>',views.DoctorScheduleCreateView.as_view(),name="manage_doctorschedule"),
    
    path('delete_doctorschedule/<str:id>/<did>',views.deleteTimeSlot,name="delete_doctorschedule"),
    path('update_doctorschedule/<id>/<sid>',views.updateDoctorSchedual,name="update_doctorschedule"),

    #active deactive staff
    path('active_staff/<id>',views.activeStaff,name="active_staff"),
    path('deactive_staff/<id>',views.deactiveStaff,name="deactive_staff"),
    path('delete_staff/<id>',views.deleteHospitalStaff,name="delete_staff"),
    #active deactive department
    path('active_department/<id>',views.activeDepartment,name="active_department"),
    path('deactive_department/<id>',views.deactiveDepartment,name="deactive_department"),
    path('delete_department/<id>',views.deleteHospitalDepartment,name="delete_department"),
    #active deactive rooms
    path('active_room/<id>',views.activeRoom,name="active_room"),
    path('deactive_room/<id>',views.deactiveRoom,name="deactive_room"),
    path('delete_room/<id>',views.deleteHospitalRoom,name="delete_room"),
    path('occupied_room',views.OccupiedRoom,name="occupied_room"),
    #active deactive delete Doctor 
    path('active_doctor/<id>',views.activeDoctor,name="active_doctor"),
    path('deactive_doctor/<id>',views.deactiveDoctor,name="deactive_doctor"),
    path('delete_doctor/<id>',views.deleteHospitalDoctor,name="delete_doctor"),
    #add media delete
    path('manage_gallery',views.manageGalleryView.as_view(),name="manage_gallery"),
    path('delete_gallery/<id>',views.deleteGallery,name="delete_gallery"),
    #active deactive delete Doctor Schedual  
    path('delete_doctorschedual/<id>/<sid>',views.deleteHospitalDoctorschedual,name="delete_doctorschedual"),
    # path('add_staff',views.addStaffView.as_view(),name="add_staff"),
    #delete price add price
    path('add_price',views.PriceCreate,name="add_price"),
    path('delete_price/<id>',views.deletePrice,name="delete_price"),
    path('hospital_reviews/',views.HospitalReviewsListView.as_view(),name="hospital_reviews"),

    re_path('verifybooking',views.verifybooking,name="verifybooking"),

    #deaprtment manage add update delete 
    path('manage_disease',views.manageDiseaseView.as_view(),name="manage_disease"),
    
    #Blog Urls
    # path('add_blog',views.addBlogView.as_view(),name="add_blog"),
    # path('list_blog',views.blogListView.as_view(),name="list_blog"),
    # path('edit_blog/<id>',views.EditBlogUpdateView.as_view(),name="edit_blog"),
    # path('active_blog/<id>',views.activeBlog,name="active_blog"),
    # path('inactive_blog/<id>',views.inactiveBlog,name="inactive_blog"),


]  