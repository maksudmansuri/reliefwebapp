from django.urls import path
from .import views
    
urlpatterns = [  
    #Time SLot Add delete
    path('time_slot',views.TimeSlotView.as_view(),name="time_slot"),
    path('delete_time_slot',views.deleteTimeSlot,name="delete_time_slot"),

    #locations country , state, city, area

    # path('find_state',views.findState,name="find_state"),
    #Edit from admin hospital lab pharmacy
    path('radmin_hospital_update/<id>',views.hospitalUpdateViews.as_view(),name="radmin_hospital_update"),
    path('radmin_lab_update/<id>',views.LabUpdateViews.as_view(),name="radmin_lab_update"),
    path('radmin_doctor_update/<id>',views.DoctorUpdateViews.as_view(),name="radmin_doctor_update"),
    path('radmin_pharmacy_update/<id>',views.PharmacyUpdateViews.as_view(),name="radmin_pharmacy_update"),
    path('radmin_patients_update/<id>',views.hospitalUpdateViews.as_view(),name="radmin_patients_update"),

    path('loaction_area',views.AddCountriesView.as_view(),name="loaction_area"),
    path('delete_country/<id>',views.deleteCountry,name="delete_country"),
    path('delete_state/<id>',views.deleteState,name="delete_state"),
    path('delete_city/<id>',views.deleteCity,name="delete_city"),
         
    #specialist hospital labs, pharmacy
    path('specialist_hospital',views.AddHospitalSpecialistView.as_view(),name="specialist_hospital"),
    path('update_specialist_hospital/<id>',views.updateHospitalSpecialist,name="update_specialist_hospital"),
    path('delete_specialist_hospital/<id>',views.deleteHospitalSpecialist,name="delete_specialist_hospital"),

    
    path('appointment',views.AppointmentListView.as_view(),name="appointment"),

    path('',views.indexListView.as_view(),name="radmin_home"),
    path('admin_hospital_all',views.HospitalallViews.as_view(),name="manage_hospital_admin"),
    path('hospital_delete_admin/<id>',views.HospitalDelete,name="hospital_delete_admin"),
    path('manage_patient_admin',views.PatientAllViews.as_view(),name="manage_patient_admin"),
    path('patient_delete_admin/<id>',views.PatientDelete,name="patient_delete_admin"),
    path('doctor_delete_admin/<id>',views.DoctorDelete,name="doctor_delete_admin"),
    path('manage_labs_admin',views.LabsAllViews.as_view(),name="manage_labs_admin"),
    path('labs_delete_admin/<id>',views.LabsDelete,name="labs_delete_admin"),
    path('manage_pharmacy_admin',views.PharmacyAllViews.as_view(),name="manage_pharmacy_admin"),
    path('pharmacy_delete_admin/<id>',views.PharmacyDelete,name="pharmacy_delete_admin"),
    path('manage_accident_admin',views.AccidentAllViews.as_view(),name="manage_accident_admin"),
    path('accident_delete_admin/<id>',views.AccidentDelete,name="accident_delete_admin"),
    
    # Appointment Hospital Labs Pharmcy  Accident
    path('hospital_appointment_admin',views.HosAppointmentAllViews.as_view(),name="hospital_appointment_admin"),
    path('labs_appointment_admin',views.LabsAppointmentAllViews.as_view(),name="labs_appointment_admin"),
    path('pha_appointment_admin',views.PhaAppointmentAllViews.as_view(),name="pha_appointment_admin"),

    #Profiel for Hospital, Labs , Pharmcy, Patient 
    path('hospital_profile_admin/<id>',views.HospitalDetailsViews.as_view(),name="hospital_profile_admin"),
    path('doctor_profile_admin/<id>',views.DoctorsBookAppoinmentViews.as_view(),name="doctor_profile_admin"),
    path('labs_profile_admin/<id>',views.LabDetailsViews.as_view(),name="labs_profile_admin"),
    path('pharmacy_profile_admin/<id>',views.PharmacyDetailsViews.as_view(),name="pharmacy_profile_admin"),
    path('patient_profile_admin/<id>',views.PatientDetailsViews.as_view(),name="patient_profile_admin"),
   
  
    # ACTIVATE DEACTIVATE HOSPITAL, DOCTOR, PATIENT, LABS, PHARMACY ,ACCIDENT
    path('hospitalactivate/<id>',views.HospitalActivate,name="hospitalactivate"),
    path('hospitaldeactivate/<id>',views.HospitalDeactivate,name="hospitaldeactivate"),
    path('patientactivate/<id>',views.PatientActivate,name="patientactivate"),
    path('patinetdeactivate/<id>',views.PatientDeactivate,name="patinetdeactivate"),
    path('pharmacyactivate/<id>',views.PharmacyActivate,name="pharmacyactivate"),
    path('pharmacydeactivate/<id>',views.PharmacyDeactivate,name="pharmacydeactivate"),
    path('labsactivate/<id>',views.LabsActivate,name="labsactivate"),
    path('labsdeactivate/<id>',views.LabsDeactivate,name="labsdeactivate"),
    path('doctorsactivate/<id>',views.DoctorsActivate,name="doctorsactivate"),
    path('doctorsdeactivate/<id>',views.DoctorsDeactivate,name="doctorsdeactivate"),
    path('accidentactivate/<id>',views.AccidentActivate,name="accidentactivate"),
    path('accidentdeactivate/<id>',views.AccidentDeactivate,name="accidentdeactivate"),

    #All Reviews
    path('reviews',views.ReviewsList.as_view(),name="reviews"),
]