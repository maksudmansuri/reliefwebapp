
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
from patient.models import Orders

from .serializers import AppointmentSerializer, HomeScreenSerializer, HospitalDoctorHomeScreenSerializer, HospitalDoctorSerialzer, HospitalDoctorsViewSerializer, HospitalHomeScreenSerializer, HospitalsSerializer, LabHomeScreenSerializer, LabsViewSerializer, OnlineDoctorserializer, PharmaHomeScreenSerializer, PharmacysViewSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000

SUCCESS = 'success'
ERROR = 'error'
DELETE_SUCCESS = 'deleted'
UPDATE_SUCCESS = 'updated'
CREATE_SUCCESS = 'created'
"""NEw APIS by pages"""

class HomeScreenView(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Specailist.objects.all().order_by('updated_at')
	pagination_class = StandardResultsSetPagination
	
	def get(self, request, format=None, **kwargs):
		spc = Specailist.objects.all().order_by('updated_at')[:10]
		specialistserializer = HomeScreenSerializer(spc,many=True)
		hos = Hospitals.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		hospitals = HospitalHomeScreenSerializer(hos,many=True)
		doc = HospitalDoctors.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		doctors = HospitalDoctorHomeScreenSerializer(doc,many=True)
		lab = Labs.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		labs = LabHomeScreenSerializer(lab,many=True)
		pharma = Pharmacy.objects.filter(is_verified = True,admin__is_active = True).order_by('updated_at')[:10]
		pharmacy = PharmaHomeScreenSerializer(pharma,many=True)

		return Response({
			"status": "success",
			'specialists': specialistserializer.data,
			'hospitals': hospitals.data,
			'doctors': doctors.data,
			'labs': labs.data,
			'Pharmas': pharmacy.data,
			
		})

"""Old APIs"""
class specialistViewSets(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	queryset = Specailist.objects.all().order_by('id')
	pagination_class = StandardResultsSetPagination
	serializer_class = HomeScreenSerializer

class ApiHospitalListAndDetailsView(ListAPIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	filter_backends = [SearchFilter,OrderingFilter]
	filter_fields = (
        'specialist',
        'city',
    )
	search_fields = ['hopital_name','specialist','city']

		# def get_queryset(self):
		# 	"""
		# 	Optionally restricts the returned purchases to a given user,
		# 	by filtering against a `username` query parameter in the URL.
		# 	"""
		# 	queryset = Hospitals.objects.filter(is_verified = True,admin__is_active = True)
		# 	spc = self.request.query_params.get('specialist')
		# 	if spc is not None:
		# 		queryset = queryset.filter(specialist=spc)
		# 	return queryset

	def get(self, request, id=None):
		# print(request.data['id'])		
		if id:
			hospital = get_object_or_404(Hospitals,id = id,is_verified = True,admin__is_active = True)
			serializer = HospitalDoctorsViewSerializer(hospital)
			print(serializer.data)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = Hospitals.objects.filter(is_verified = True,admin__is_active = True)
		serializer = HospitalHomeScreenSerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class HospitalDoctorDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination

	def get(self,request,id=None,did=None):
		if id or did:
			hospitaldoctors = HospitalDoctors.objects.get(id=id,admin__is_active=True)			
			serializer = HospitalDoctorSerialzer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospital = HospitalDoctors.objects.filter(is_verified=True,admin__is_active = True)
		serializer = HospitalDoctorHomeScreenSerializer(hospital, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
	
class APIDoctorListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	def get(self,request,id=None,did=None):
		if id:
			hospitaldoctors = HospitalDoctors.objects.get(id=id,is_active=True)			
			serializer = HospitalDoctorSerialzer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospitaldoctors = HospitalDoctors.objects.filter(is_active=True)
		serializer = HospitalDoctorHomeScreenSerializer(hospitaldoctors, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class APIOnlineDoctorListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	def get(self,request,id=None,did=None):
		if id:
			hospitaldoctors = HospitalDoctors.objects.get(id=id,admin__is_active=True,is_virtual_available=True)
			serializer = HospitalDoctorSerialzer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospitaldoctors = HospitalDoctors.objects.filter(is_virtual_available=True,admin__is_active=True)
		serializer = HospitalDoctorHomeScreenSerializer(hospitaldoctors, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

class APIHomevisitDoctorListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	def get(self,request,id=None,did=None):
		if id:
			hospitaldoctors = HospitalDoctors.objects.get(id=id,admin__is_active=True,is_homevisit_available=True)			
			serializer = HospitalDoctorSerialzer(hospitaldoctors)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		hospitaldoctors = HospitalDoctors.objects.filter(is_homevisit_available=True,admin__is_active=True)
		serializer = HospitalDoctorHomeScreenSerializer(hospitaldoctors, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


"""
LAbs Views
"""

class ApiLabsListAndDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('lab_name','specialist','city')

	def get(self, request, id=None):
		if id:
			lab = get_object_or_404(Labs,id = id,is_verified = True,admin__is_active = True)
			serializer = LabsViewSerializer(lab)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		labs = Labs.objects.all()
		serializer = LabHomeScreenSerializer(labs, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

"""
Pharmacy Views
"""

class ApiPharmacyListAndDetailsView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	filter_backends = (SearchFilter,OrderingFilter)
	search_fields = ('lab_name','specialist','city')

	def get(self, request, id=None):
		if id:
			pharmacy = get_object_or_404(Pharmacy,id = id,is_verified = True,admin__is_active = True)
			serializer = PharmacysViewSerializer(pharmacy)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		pharmacy = Pharmacy.objects.all()
		serializer = PharmaHomeScreenSerializer(pharmacy, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

"""
Appointment Views
"""
class AppointmentListView(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	pagination_class = StandardResultsSetPagination
	def get(self,request,id=None):
		if id:
			order = Orders.objects.get(id=id)			
			serializer = AppointmentSerializer(order)
			return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

		orders = Orders.objects.filter( patient  = request.user )
		serializer = AppointmentSerializer(orders, many=True)
		return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


