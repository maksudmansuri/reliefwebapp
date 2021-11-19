from accounts import profilePic
from django.urls import path
from .import views,logoutview
from .import adminView
from .import profilePic

urlpatterns = [  
    path("verifyOTP/<phone>", views.verifyOTP, name="OTP_Gen"),
    path("verifyPhone/<phone>", views.verifyPhone, name="verifyPhone"),
    path("resendOTP/<phone>", views.resendOTP, name="resendOTP"),
    path('login', views.dologin,name='dologin'),
    path('logout', logoutview.logout_view,name='dologout'),
    path('dosingup', views.adminSingup,name='dosingup'),
    path('hospitalsingup', views.HospitalSingup.as_view(),name='hospitalsingup'),
    path('doctorsingup', views.DoctorSingup.as_view(),name='doctorsingup'),
    path('Authorizedsingup', views.AuthorizedSingup.as_view(),name='Authorizedsingup'),
    
    path('patientsingup', views.PatientSingup.as_view(),name='patientsingup'),
    path('patient-register-step-1/<user_id>', views.PatientSingupStep1.as_view(),name='patientregisterstep1'),
    path('patient-register-step-2/<user_id>', views.PatientSingupStep2.as_view(),name='patientregisterstep2'),
    path('patient-register-step-3/<user_id>', views.PatientSingupStep3.as_view(),name='patientregisterstep3'),
    # path('patient-register-step-4/<user_id>', views.PatientSingupStep4.as_view(),name='patientregisterstep4'),
    # path('patient-register-step-5/<user_id>', views.PatientSingupStep5.as_view(),name='patientregisterstep5'),
    
    
    path('labsingup', views.LabSingup.as_view(),name='labsingup'),
    path('pharmacysingup', views.PharmacySingup.as_view(),name='pharmacysingup'),
    path('activate/<uidb64>/<token>', views.activate,name='activate'),

    #adminHOD singup PAge i=only access by superuser
    path('adminsingup',adminView.AdminSingup.as_view(),name="adminsingup" ),
    #upload profile pic
    path('profile_picUpload',profilePic.profilePicUpload,name="profile_picUpload"),
    
   
    
]