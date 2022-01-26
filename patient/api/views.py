
from django.contrib.auth import models
from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import HospitalDoctors, Hospitals, Labs, Pharmacy, Specailist
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter
from front.models import RatingAndComments
from patient.models import OrderBooking, Orders

from .serializers import AppointmentSerializer, HomeScreenSerializer, HospitalDoctorHomeScreenSerializer, HospitalDoctorSerialzer, HospitalDoctorsViewSerializer, HospitalHomeScreenSerializer,LabHomeScreenSerializer, LabsViewSerializer, PharmaHomeScreenSerializer, PharmacysViewSerializer, RatingListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'
"""NEw APIS by pages"""

class HomeScreenView(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Specailist.objects.all().order_by('updated_at')
	pagination_class = StandardResultsSetPagination
	
	def get_serializer_class(self):
		if self.action == 'list':
			spc = Specailist.objects.all().order_by('updated_at')
			specialistserializer = HomeScreenSerializer(spc,many=True)
			hos = Hospitals.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
			hospitals = HospitalHomeScreenSerializer(hos,many=True)
			return Response({
			"status": "success",
			'specialists': specialistserializer,
			'hospitals': hospitals,		
			
		})
		if self.action == 'retrieve':
			serializer = HomeScreenSerializer
			return serializer
	
	# def get(self, request, format=None, **kwargs):
	# 	spc = Specailist.objects.all().order_by('updated_at')
	# 	specialistserializer = HomeScreenSerializer(spc,many=True)
	# 	hos = Hospitals.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
	# 	hospitals = HospitalHomeScreenSerializer(hos,many=True)
		# doc = HospitalDoctors.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		# doctors = HospitalDoctorHomeScreenSerializer(doc,many=True)
		# lab = Labs.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		# labs = LabHomeScreenSerializer(lab,many=True)
		# pharma = Pharmacy.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		# pharmacy = PharmaHomeScreenSerializer(pharma,many=True)

		# return Response({
		# 	"status": "success",
		# 	'specialists': specialistserializer.data,
		# 	'hospitals': hospitals.data,
		# 	# 'doctors': doctors.data,
		# 	# 'labs': labs.data,
		# 	# 'Pharmas': pharmacy.data,
			
		# })

class specialistViewSets(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Specailist.objects.all().order_by('id')
	pagination_class = StandardResultsSetPagination
	serializer_class = HomeScreenSerializer

class ApiHospitalListAndDetailsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = Hospitals.objects.filter(is_verified = True,admin__is_active = True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = HospitalHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = HospitalDoctorsViewSerializer
			return serializer
		return HospitalDoctorsViewSerializer	

class HospitalDoctorDetailsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = HospitalDoctors.objects.filter(is_verified = True,admin__is_active = True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = HospitalDoctorHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = HospitalDoctorSerialzer
			return serializer
		return HospitalDoctorSerialzer

class APIOnlineDoctorListView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = HospitalDoctors.objects.filter(admin__is_active=True,is_virtual_available=True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = HospitalDoctorHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = HospitalDoctorSerialzer
			return serializer
		return HospitalDoctorSerialzer

class APIHomevisitDoctorListView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = HospitalDoctors.objects.filter(admin__is_active=True,is_homevisit_available=True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = HospitalDoctorHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = HospitalDoctorSerialzer
			return serializer
		return HospitalDoctorSerialzer

"""
LAbs Views
"""

class ApiLabsListAndDetailsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = Labs.objects.filter(is_verified = True,admin__is_active = True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = LabHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = LabsViewSerializer
			return serializer
		return LabsViewSerializer

"""
Pharmacy Views
"""

class ApiPharmacyListAndDetailsView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = Pharmacy.objects.filter(is_verified = True,admin__is_active = True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = PharmaHomeScreenSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = PharmacysViewSerializer
			return serializer
		return PharmacysViewSerializer


"""
Appointment Views
"""
class AppointmentListView(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	def get_queryset(self):
		return OrderBooking.objects.filter(patient  = self.request.user)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = AppointmentSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = AppointmentSerializer
			return serializer
		return AppointmentSerializer


"""Rating and Commennts"""

class RatingViesStates(viewsets.ModelViewSet):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	queryset = RatingAndComments.objects.filter(is_active = True)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']
	def get_serializer_class(self):
		if self.action == 'list':
			serializer = RatingListSerializer
			return serializer
		if self.action == 'retrieve':
			serializer = RatingListSerializer
			return serializer
		return AppointmentSerializer

