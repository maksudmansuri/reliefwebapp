from django.urls import path
from django.urls.conf import re_path
from .import views
  
urlpatterns = [  
    path('',views.PharmaDashboardViews.as_view(),name="pharmacy_home"), 
    path('appointment_list',views.PharmaDashboardListViews.as_view(),name="appointment_list"), 
    path('pharmacy_update',views.PharmacyUpdateViews.as_view(),name="pharmacy_update"),
    path('view_pharmacy_appointment',views.ViewPharmacyAppointmentViews.as_view(),name="view_pharmacy_appointment"),
    path('updload_invoice_pharmacy/<id>',views.UpdloadInvoicePharmacy,name="updload_invoice_pharmacy"),
    path('pharmacy_manage_gallery',views.ManageMainGalleryView.as_view(),name="pharmacy_manage_gallery"),
    path('delete_pharma_gallery',views.deleteMainGallery,name="delete_pharma_gallery"),
    path('delete_pharmacy_appointment/<id>',views.deleteServicesViews,name="delete_pharmacy_appointment"),
    re_path('verifypharmacybooking',views.verifypharmacybooking,name="verifypharmacybooking"),
    path('pharmacy_reviews/',views.PharmacyReviewsListView.as_view(),name="pharmacy_reviews"),

     #previous Patients or Tests
    path('ph_accept_apt/<id>',views.AcceptAPT,name="ph_accept_apt"),
    path('ph_accept_otp/<id>',views.AcceptOTP,name="ph_accept_otp"),
    path('ph_reject_apt/<id>',views.RejectedAPT,name="ph_reject_apt"),
  
]