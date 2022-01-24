from sre_constants import SUCCESS
from django.urls import path
from .import views
 
urlpatterns = [   
    path('',views.FrontView.as_view(),name="front_home"),

    #search for all categories
    path('search_hospital',views.SearchHospitalView.as_view(),name="search_hospital"),
    path('search_online_hospital',views.SearchOnlineHospitalView.as_view(),name="search_online_hospital"),
    path('search_homevisit_hospital',views.SearchHomeVisitHospitalView.as_view(),name="search_homevisit_hospital"),
    path('search_doctor',views.SearchDoctorView.as_view(),name="search_doctor"),
    path('search_ambulance_hospital',views.SearchAmbulanceHospitalView.as_view(),name="search_ambulance_hospital"),
    path('search_Labs',views.SearchLabView.as_view(),name="search_Labs"),
    path('search_pharmcy',views.SearchPharmacyView.as_view(),name="search_pharmcy"),
    path('search_blood_donor',views.BLoodDonorList.as_view(),name="search_blood_donor"),
    path('specilist_hospitals/<hid>',views.SearcCathHospitalView.as_view(),name="specilist_hospitals"),
    path('specilist_doctor/<hid>',views.SearcCathDoctorView.as_view(),name="specilist_doctor"),

    #doctor_details
    path('doctor_details/<id>', views.DoctorDetailsViews.as_view(), name="doctor_details"),

    #profiles Hospital
    path('hospital_details/<id>', views.HospitalDetailsViews.as_view(), name="hospital_details"),
    path('ratingandcomment', views.HospitalComments.as_view(), name="ratingandcomment"),
    
    path('delete_reviews/<id>',views.deleteReviews,name="delete_reviews"),

    path('bookappoinment/<id>', views.DoctorsBookAppoinmentViews.as_view(), name="bookappoinment"),
    #Profile Labs
    path('lab_details/<id>', views.LabDetailsViews.as_view(), name="lab_details"),
    path('lab_bookappoinment/<id>', views.LabAppoinmentViews.as_view(), name="lab_bookappoinment"),
    path('bookappoinment_final', views.BookAnAppointmentViews.as_view(), name="bookappoinment_final"),

    #Profile Labs
    path('pharmacy_details/<id>', views.PharmacyDetailsViews.as_view(), name="new_pharmacy_details"),

    #blog list and details
    path('blog_list',views.BlogListView.as_view(),name="blog_list"),
    path('blog_details/<pk>',views.BlogDetailsView.as_view(),name="blog_details"),
   
    # path('bookappoinment/<id>/<did>', views.DoctorsBookAppoinmentViews.as_view(), name="bookappoinment"),

    #payment process
    path('invoice/<id>', views.InvoiceViews.as_view(), name="invoice"),
    path('invoice_pdf/<id>', views.pdfgenerator, name="invoice_pdf"),
    
    
    # path('blood_donor_list', views.BLoodDonorList.as_view(), name="blood_donor_list"),
    

    #SUCCESS Full pages
    path('donorrequest', views.BloodRequestView.as_view(), name="donorrequest"),
    path('successfullpage/<id>', views.DonorRequestDone.as_view(), name="successfullpage"),
    #extra for json
    # path('scheduledatechange', views.ScheduleDateChange, name="scheduledatechange"),
]