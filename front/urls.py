from django.urls import path
from .import views
 
urlpatterns = [   
    path('',views.FrontView.as_view(),name="front_home"),
    path('search_hospital',views.SearchHospitalView.as_view(),name="search_hospital"),
     
    path('hospital_details/<id>', views.HospitalDetailsViews.as_view(), name="hospital_details"),

    path('blog_list',views.BlogListView.as_view(),name="blog_list"),
    path('blog_details/<pk>',views.BlogDetailsView.as_view(),name="blog_details"),
   
    path('bookappoinment/<id>/<did>', views.DoctorsBookAppoinmentViews.as_view(), name="bookappoinment"),

    #extra for json
    # path('scheduledatechange', views.ScheduleDateChange, name="scheduledatechange"),
]