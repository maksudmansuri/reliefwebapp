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
    
    #patient list ,add ,update ,delete
    path('doc_manage_patient',views.managePatientView.as_view(),name="doc_manage_patient"),
    path('doc_update_patient',views.updatePatientView,name="doc_update_patient"),
    path('delete__doc_patient/<id>',views.deleteDoctorPatient,name="delete__doc_patient"),
    
    # Appointment Update Delete treatment
    path('doc_manage_appointment',views.manageAppointmentView.as_view(),name="doc_manage_appointment"),
    # path('update_appointment',views.updateAppointment,name="update_appointment"),
    path('doc_delete_appointment/<id>',views.dateleAppointment,name="doc_delete_appointment"),
    
     #List  Add Update Doctor schedual  Doctor
    path('doc_manage_doctorschedule',views.DoctorScheduleCreateView.as_view(),name="doc_manage_doctorschedule"),
    
    path('doc_delete_doctorschedule/<str:id>/<did>',views.deleteTimeSlot,name="doc_delete_doctorschedule"),

    
    re_path('doc_verifybooking',views.verifybooking,name="doc_verifybooking"),
    path('doctor_reviews/',views.DoctorReviewsListView.as_view(),name="doctor_reviews"),
    
    #Blog Urls
    path('add_blog',views.addBlogView.as_view(),name="add_blog"),
    path('list_blog',views.blogListView.as_view(),name="list_blog"),
    path('edit_blog/<id>',views.EditBlogUpdateView.as_view(),name="edit_blog"),
    path('active_blog/<id>',views.activeBlog,name="active_blog"),
    path('inactive_blog/<id>',views.inactiveBlog,name="inactive_blog"),

    path('manage_disease',views.manageDiseaseView.as_view(),name="doc_manage_disease"),

]  