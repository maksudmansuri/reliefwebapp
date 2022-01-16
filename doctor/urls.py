from django.urls import path
from django.urls.conf import re_path
from .import views
from patient import views as patientView
from front import views as frontView

urlpatterns = [   
    # path('',views.indexView,name="doctor_home"),
    path('',views.doctordDashboardViews.as_view(),name="doctor_dashboard"),
    path('doctor_update',views.doctorUpdateViews.as_view(),name="doctor_update"),
    path('doctor_profile',frontView.HospitalDetailsViews.as_view(),name="doctor_profile"),

    #Order Booking for doctor ,Lab ,pharmacy, 
    #doctor
    path('doc_accept_apt/<id>',views.AcceptAPT,name="doc_accept_apt"),
    path('doc_accept_otp/<id>',views.AcceptOTP,name="doc_accept_otp"),
    path('doc_reject_apt/<id>',views.RejectedAPT,name="doc_reject_apt"),

    #review list
    path('doc_reviews',views.ReviewsList.as_view(),name="doc_reviews"),
    
    
    # for treatment tab menu Treatment includes Diseas , Medicine(with time) , Reports , Follow ups dates , Exercise 
 

    path('doc_manage_relief_patient',views.manageReliefPatientViews.as_view(),name="doc_manage_relief_patient"),
    path('doc_relief_patient_profile/<id>',views.ReliefPatientViewsProfile.as_view(),name="doc_relief_patient_profile"),
    path('doc_relief_patient_files/<id>',views.ReliefPatientViewsFiles,name="doc_relief_patient_files"),
    path('doc_manage_treatment/<id>',views.manageTreatmentViews.as_view(),name="doc_manage_treatment"),
    path('doc_delete__relief_doctor_patient/<id>',views.deleteReliefDoctorPatient,name="doc_delete__relief_doctor_patient"),


    # #Staff list ,add ,update ,delete
    # path('manage_staff',views.manageStaffView.as_view(),name="manage_staff"),
    # path('update_staff',views.updateStaff,name="update_staff"),
    
    #patient list ,add ,update ,delete
    path('doc_manage_patient',views.managePatientView.as_view(),name="doc_manage_patient"),
    path('doc_update_patient',views.updatePatientView,name="doc_update_patient"),
    path('delete__doc_patient/<id>',views.deleteDoctorPatient,name="delete__doc_patient"),
    
    # Appointment Update Delete treatment
    path('doc_manage_appointment',views.manageAppointmentView.as_view(),name="doc_manage_appointment"),
    # path('update_appointment',views.updateAppointment,name="update_appointment"),
    path('doc_delete_appointment/<id>',views.dateleAppointment,name="doc_delete_appointment"),
    
    #deaprtment manage add update delete 
    # path('manage_department',views.manageDepartmentclassView.as_view(),name="manage_department"),
    # path('update_department',views.updateDepartment,name="update_department"),
 
    #deaprtment manage add update delete 
    # path('manage_room',views.manageRoomclassView.as_view(),name="manage_room"),
    # path('update_room/<id>',views.updateRoom,name="update_room"),
    
    # #Ambulance manage add update delete 
    # path('manage_ambulance',views.manageAmbulanceclassView.as_view(),name="manage_ambulance"), 
    # path('update_ambulance',views.updateAmbulance,name="update_ambulance"),
    # path('delete_ambulance/<id>',views.deleteAmbulance,name="delete_ambulance"),


    # Add Doctor Update Doctor
    # path('manage_doctor',views.manageDoctorView.as_view(),name="manage_doctor"),
    # path('update_doctor',views.updateDoctor,name="update_doctor"),

    # Price Doctor Update Doctor
    # path('manage_price',views.managePricesView.as_view(),name="manage_price"),
    # path('update_service_price',views.updateServicePrice,name="update_service_price"),
    # path('delete_service_price/<id>',views.deleteServicePrice,name="delete_service_price"),

     #List  Add Update Doctor schedual  Doctor
    path('doc_manage_doctorschedule/<id>',views.DoctorScheduleCreateView.as_view(),name="doc_manage_doctorschedule"),
    
    path('doc_delete_doctorschedule/<str:id>/<did>',views.deleteTimeSlot,name="doc_delete_doctorschedule"),
    path('doc_update_doctorschedule/<id>/<sid>',views.updateDoctorSchedual,name="doc_update_doctorschedule"),

    #active deactive staff
    # path('active_staff/<id>',views.activeStaff,name="active_staff"),
    # path('deactive_staff/<id>',views.deactiveStaff,name="deactive_staff"),
    # path('delete_staff/<id>',views.deletedoctorStaff,name="delete_staff"),
    #active deactive department
    # path('active_department/<id>',views.activeDepartment,name="active_department"),
    # path('deactive_department/<id>',views.deactiveDepartment,name="deactive_department"),
    # path('delete_department/<id>',views.deletedoctorDepartment,name="delete_department"),
    #active deactive rooms
    # path('active_room/<id>',views.activeRoom,name="active_room"),
    # path('deactive_room/<id>',views.deactiveRoom,name="deactive_room"),
    # path('delete_room/<id>',views.deletedoctorRoom,name="delete_room"),
    # path('occupied_room',views.OccupiedRoom,name="occupied_room"),
    #active deactive delete Doctor 
    path('doc_active_doctor/<id>',views.activeDoctor,name="doc_active_doctor"),
    path('doc_deactive_doctor/<id>',views.deactiveDoctor,name="doc_deactive_doctor"),
    path('doc_delete_doctor/<id>',views.deleteDoctor,name="doc_delete_doctor"),
    #add media delete
    # path('doc_manage_gallery',views.manageGalleryView.as_view(),name="doc_manage_gallery"),
    # path('doc_delete_gallery/<id>',views.deleteGallery,name="doc_delete_gallery"),
    #active deactive delete Doctor Schedual  
    path('doc_delete_doctorschedual/<id>/<sid>',views.deleteDoctorschedual,name="doc_delete_doctorschedual"),
    # path('add_staff',views.addStaffView.as_view(),name="add_staff"),
    #delete price add price
    # path('add_price',views.PriceCreate,name="add_price"),
    # path('delete_price/<id>',views.deletePrice,name="delete_price"),
    
    re_path('doc_verifybooking',views.verifybooking,name="doc_verifybooking"),
    path('doctor_reviews/',views.DoctorReviewsListView.as_view(),name="doctor_reviews"),
    
    #Blog Urls
    path('add_blog',views.addBlogView.as_view(),name="add_blog"),
    path('list_blog',views.blogListView.as_view(),name="list_blog"),
    path('edit_blog/<id>',views.EditBlogUpdateView.as_view(),name="edit_blog"),
    path('active_blog/<id>',views.activeBlog,name="active_blog"),
    path('inactive_blog/<id>',views.inactiveBlog,name="inactive_blog"),


]  