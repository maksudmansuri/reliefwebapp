from django.urls import path
from .import views

urlpatterns = [   
    path('',views.FrontView.as_view(),name="front_home"),
    path('search_hospital',views.SearchHospitalView.as_view(),name="search_hospital"),
    
    
    path('blog_list',views.BlogListView.as_view(),name="blog_list"),
    path('blog_details/<pk>',views.BlogDetailsView.as_view(),name="blog_details"),
   

  
]