"""relief URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, re_path
from accounts import adminView
from relief import settings
from django.conf.urls.static import static
from accounts import views as accViews
from django.contrib.auth import views as auth_views
from patient import PatientPassword as patientAuth
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    # path('404',accViews.FourZeroFour , name='404'),
    path('admin/', admin.site.urls),    
    path('radmin/', include("radmin.urls")),
    path('', include("front.urls")),
    path('accounts/', include("accounts.urls")),
    path('hospital/', include("hospital.urls")),    
    path('doctor/', include("doctor.urls")),    
    path('patient/', include("patient.urls")),  
    path('lab/', include("lab.urls")),
    path('pharmacy/', include("pharmacy.urls")),
    #Api urls
    path('api/accounts/',include("accounts.api.urls")),
    path('api/patient/',include("patient.api.urls")),    
    # path('hospital_profile',profileview.hospitalProfileViews.as_view(),name="hospital_profile"),
    #APIs Docs
  
    path('docs/',include_docs_urls(title='BookingAppAPI'),name="docs"),
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #password reset and change
    path('password_change/done',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),name='password_change_done'),

    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),name='password_change',),

    path('password_change_patient/done',patientAuth.PasswordChangeDonePatientView.as_view(template_name='password_change_done_patient.html'),name='password_change_done_patient'),

    path('password_change_patient/',patientAuth.PasswordChangePatientView.as_view(template_name='password_change_patient.html'),name='password_change_patient'),

    path('password_reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),

    path('reset/done',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    
     
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
