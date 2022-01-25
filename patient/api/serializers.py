from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import  HospitalDoctors, Hospitals, Labs, Pharmacy, Specailist
from front.models import RatingAndComments
from hospital.models import AmbulanceDetails, DoctorSchedule, HospitalMedias, HospitalRooms, ServiceAndCharges, TimeSlot
from lab.models import Medias
from patient.models import Booking, LabTest, OrderBooking, Orders, PicturesForMedicine, Slot
from radmin.models import Disease, HospitalDisease


	
"""Serilizer by pages"""
class HomeScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Specailist
		fields = ['pk','specialist_name','hover_icon','specialist_icon']

class InsideScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Specailist
		fields = ['specialist_name']

class ratingSerilizers(serializers.ModelSerializer):
	class Meta:
		model = RatingAndComments
		fields =['pk','patient','HLP','rating','comment'] 

class HospitalHomeScreenSerializer(serializers.ModelSerializer):
	comment_to = ratingSerilizers
	class Meta:
		model = Hospitals
		fields = ['pk','hopital_name','address1','address2','city','pin_code','state','profile_pic']
	
	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance)
		response['specialist'] = InsideScreenSerializer(instance.specialist).data
		return response

class HospitalDoctorHomeScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = HospitalDoctors
		fields = ['pk','fisrt_name','last_name','address','city','pin_code','state','profile_pic','degree','gender','is_virtual_available','is_online']

	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance)
		response['specialist'] = InsideScreenSerializer(instance.specialist).data
		return response
	
class LabHomeScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Labs
		fields = ['pk','lab_name','address','city','pin_code','state','profile_pic']

class PharmaHomeScreenSerializer(serializers.ModelSerializer):
	class Meta:
		model = Pharmacy
		fields = ['pk','pharmacy_name','address','city','pin_code','state','profile_pic']


"""ALl OLD Serializers"""

class TimeSlotSerializer(serializers.ModelSerializer):

	class Meta:
		model = TimeSlot
		fields = ['pk','schedule']

class DoctorSchedulesSerializer(serializers.ModelSerializer):

	class Meta:
		model = DoctorSchedule
		fields = ['pk','scheduleDate','is_active','is_booked']
	
	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance)
		response['timeslot'] = TimeSlotSerializer(instance.timeslot).data
		# response['hospital'] = HospitalsSerializer(instance.hospital).data
		return response

class HospitalDoctorSerialzer(serializers.ModelSerializer):
	# schedules = DoctorSchedulesSerializer(many=True)
	class Meta:
		model = HospitalDoctors
		fields = ['pk','name_title','fisrt_name','last_name','address','city','pin_code','state','profile_pic','degree','gender','about','dob','opd_charges','home_charges','emergency_charges','online_charges','is_homevisit_available','is_virtual_available','is_online']

	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance)
		response['specialist'] = InsideScreenSerializer(instance.specialist).data
		if instance.is_hospital_added:
			response['hospital'] = HospitalHomeScreenSerializer(instance.hospital).data
		return response

class MediaHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = HospitalMedias
		fields = ['pk','media_type','media_content','media_desc']

class RoomsPriceSerializer(serializers.ModelSerializer):
	class Meta:
		model = HospitalRooms
		fields = ['pk','rooms_price']

class RoomsHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = HospitalRooms
		fields = ['pk','room_no']

		def to_representation(self, instance):
			response = super().to_representation(instance)
			print(instance)
			response['room'] = RoomsPriceSerializer(instance.disease).data
			return response

class OrderHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderBooking
		fields = "__all__"

class DiseaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Disease
		fields = ['pk','name','d_icon']

class DiseaseHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = HospitalDisease
		fields = ['pk']

		def to_representation(self, instance):
			response = super().to_representation(instance)
			print(instance)
			response['disease'] = DiseaseSerializer(instance.disease).data
			return response

class ambulanceHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = AmbulanceDetails
		fields = ['pk','vehicle_type']

class HospitalDoctorsViewSerializer(serializers.ModelSerializer):
	hospitalstaffdoctors = HospitalDoctorSerialzer(many=True)	
	hospitalmedia = MediaHospitalSerializer(many=True)
	hospitalrooms = RoomsHospitalSerializer(many=True)
	hospitaldisease = DiseaseHospitalSerializer(many=True)	
	hospitalambulance = ambulanceHospitalSerializer(many=True)

	class Meta:
		model = Hospitals
		fields = ['hopital_name','about','address1','address2','city','pin_code','state','country','profile_pic','establishment_year','hospitalstaffdoctors','hospitalmedia','hospitalrooms','hospitaldisease','hospitalambulance']


		def to_representation(self, instance):
			response = super().to_representation(instance)
			print(instance)
			response['specialist'] = InsideScreenSerializer(instance.specialist).data
			return response
			
""""hospital deatl end"""	
class DoctorDetailSerialzer(serializers.ModelSerializer):

	class Meta:
		model = HospitalDoctors
		fields = "__all__"	
"""
Appointment Serializers
"""
class ServicesSerializer(serializers.ModelSerializer):

	class Meta:
		model = ServiceAndCharges
		fields = "__all__"

class HospitalForBookingSerializer(serializers.ModelSerializer):

	class Meta:
		model = Booking
		fields = "__all__"
	
	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['service_name'] = ServicesSerializer(instance.service).data
		return response

class LabTestserializer(serializers.ModelSerializer):

	class Meta:
		model = LabTest
		fields = "__all__"

	def to_representation(self, instance):
		response = super().to_representation(instance)
		response['service_name'] = ServicesSerializer(instance.service).data
		return response

class LabsForBookingserializer(serializers.ModelSerializer):
	labtest = LabTestserializer(many=True)

	class Meta:
		model = Slot
		fields = ['id','patient','for_whom','lab','amount','applied_date','applied_time','is_applied','status','accepted_date','taken_date','rejected_date','is_rejected','is_taken','is_accepted','is_cancelled','modified_time','modified_date','add_note','report','desc','send_to_doctor','is_active','created_at','updated_at','labtest']
			
class PharmacyForBookingserializer(serializers.ModelSerializer):

	class Meta:
		model = PicturesForMedicine
		fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):

	class Meta:
		model = Orders
		fields = ['id','patient','service','bookingandlabtest','booking_for','amount','status','created_at','updated_at','is_cancelled','is_booking_Verified','is_taken','counter','taken_date_time']

	def to_representation(self, instance):
		response = super().to_representation(instance)
		print(instance.booking_for)
		if instance.booking_for == "1":
			booking = get_object_or_404(Booking,id=int(instance.bookingandlabtest))
			print(booking)
			response['booking'] = HospitalForBookingSerializer(booking).data
		if instance.booking_for == "2":
			slot = get_object_or_404(Slot,id=int(instance.bookingandlabtest))
			response['slot'] = LabsForBookingserializer(slot).data
		if instance.booking_for == "3":
			pictureformedicine = get_object_or_404(PicturesForMedicine,id=int(instance.bookingandlabtest))
			response['pictureformedicine'] = PharmacyForBookingserializer(pictureformedicine).data
		return response

"""
Labs serializers
"""
class MediaHospitalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Medias
		fields = ['pk','media_type','media_content','media_desc']

class LabsViewSerializer(serializers.ModelSerializer):
	lab_media = MediaHospitalSerializer(many=True)
	class Meta:
		model = Labs
		fields = ['lab_name','about','address','pin_code','city','state','profile_pic','establishment_year','lab_media']
	
"""
Pharmacy serializers
"""
class PharmacysViewSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Pharmacy
		fields = ['pharmacy_name','about','address','pin_code','city','state','profile_pic','establishment_year','pharma_media']
	

	