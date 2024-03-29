from io import StringIO
from re import escape
from typing import List
from django.contrib.auth.models import User
from django.http import request
from django.http.request import HttpRequest
from accounts import models
from chat.models import Notification
from front.models import RatingAndComments
from patient.models import Booking, LabTest, OrderBooking, Orders, Slot, TreatmentReliefPetient, patientFile, phoneOPTforoders
from django.urls.base import reverse
from hospital import urls
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.contrib.auth import get_user_model
from accounts import views
from django.shortcuts import get_object_or_404, render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from hospital.models import AmbulanceDetails, Blog, ContactPerson, DepartmentPhones, Departments, DoctorSchedule, HospitalMedias, HospitalRooms, HospitalServices, HospitalStaffDoctorSchedual, HospitalStaffs, HospitalsPatients, Insurances, RoomOrBadTypeandRates, ServiceAndCharges, TimeSlot
from accounts.models import CustomUser, HospitalDoctors, HospitalPhones, Hospitals, OPDTime, Patients, Specailist
from django.urls import reverse
from datetime import datetime, timedelta
import pytz
from django.core.paginator import Paginator

from radmin.models import Disease, HospitalDisease
IST = pytz.timezone('Asia/Kolkata')
from django.db.models import Q
# Create your views here. 
def OccupiedRoom(request):
    id= request.POST.get('a_id')
    room = get_object_or_404(HospitalRooms,id=id)
    if room.occupied:
        room.occupied = False
    else:
        room.occupied = True
    room.save()
    return HttpResponse("Ok")

class hospitaldDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try: 
            hospital = Hospitals.objects.get(admin=request.user.id)
            showdate = datetime.now(tz=IST).date()
            showtime = datetime.now(tz=IST).time()
             # deactivating all old appoinments
            old_appointments = OrderBooking.objects.filter(applied_date__lt=showdate)
            for apt in old_appointments:
                if apt.is_taken == False and apt.is_otp_verified == False and apt.is_active == True and apt.is_cancelled == False and apt.is_rejected == False:
                    apt.is_active = False
                    apt.status = "NO RESPONSE FROM YOU"
                    apt.is_refund_now == True
                    apt.save()
             #Deactivate today appointmnet
            today_old_apt = OrderBooking.objects.filter(applied_date=showdate).filter(applied_time__lt=showtime)
            for apt in today_old_apt:
                if apt.is_taken == False and apt.is_otp_verified == False and apt.is_active == True and apt.is_cancelled == False and apt.is_rejected == False:
                    apt.is_active = False
                    apt.status = "NO RESPONSE FROM YOU"
                    apt.is_refund_now == True
                    apt.save()
            bookings = OrderBooking.objects.filter(HLP=hospital.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,is_rejected = False).order_by('applied_time')

            upcoming_bookings = OrderBooking.objects.filter(HLP=hospital.admin,is_taken=False,is_otp_verified=False,is_active=True,is_cancelled = False,is_rejected = False).filter(applied_date__gte=showdate).order_by('applied_date')
# filter(applied_time__gte = showtime)
            bookings_now = OrderBooking.objects.filter(HLP=hospital.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,applied_date=showdate,is_rejected = False).order_by('applied_date')
            contacts = HospitalPhones.objects.filter(hospital=hospital)
            insurances = Insurances.objects.filter(hospital=hospital)
            rooms = HospitalRooms.objects.filter(is_active=True,hospital=request.user.hospitals)
            specailists = Specailist.objects.all()

       

            if hospital.hopital_name and hospital.about and hospital.address1 and hospital.city and hospital.pin_code and hospital.state and hospital.country and hospital.landline and hospital.registration_proof and hospital.profile_pic and hospital.establishment_year and hospital.registration_number and hospital.alternate_mobile:              
                param = {'bookings':bookings,'bookings_now':bookings_now,'upcoming_bookings':upcoming_bookings}
                return render(request,"hospital/newindex.html",param)
            
            else:
                messages.add_message(request,messages.ERROR,"Some detail still Missing !")
                param={'hospital':hospital,'insurances':insurances,'contacts':contacts,'specailists':specailists}
                return render(request,"hospital/doctor-profile-settings.html",param)
        except Exception as e:
            return HttpResponse(e)
    
    def post(self, request, *args, **kwargs):
        hopital_name = request.POST.get("hopital_name")
        specialist = request.POST.get("specialist")
        profile_pic = request.FILES.get("profile_pic")

        firm = request.POST.get("firm")
        about = request.POST.get("about")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = "Gujarat"
        country = "India"
        landline = request.POST.get("landline")
        establishment_year = request.POST.get("establishment_year")
        registration_number = request.POST.get("registration_number")
        registration_proof = request.FILES.get("registration_proof")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        website = request.POST.get("website")
        #contact detail
        hospital_mobile_list= request.POST.getlist("hospital_mobile[]")
        hospital_email_list = request.POST.getlist("hospital_email[]")
        #insuarance
        insurance_type_list = request.POST.getlist("insurance_type[]")
        insurance_name_list = request.POST.getlist("insurance_name[]")
        #hidden Ids from for loop
        insurances_id = request.POST.getlist("insurances_id[]")
        contacts_id = request.POST.getlist("contacts_id[]")
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        # Sunday = request.POST.get("Sunday")
        # Monday = request.POST.get("Monday")
        # Tuesday = request.POST.get("Tuesday")
        # Wednesday = request.POST.get("Wednesday")
        # Thursday = request.POST.get("Thursday")
        # Friday = request.POST.get("Friday")
        # Saturday = request.POST.get("Saturday")
        # Sunday = request.POST.get("Sunday")
        # opening_time1 = request.POST.get("opening_time")
        # opening_time = datetime.strptime(opening_time1,"%H:%M").time()
        # close_time1 = request.POST.get("close_time")
        # close_time = datetime.strptime(close_time1,"%H:%M").time()
        # break_start_time1 = request.POST.get("break_start_time")
        # break_start_time = datetime.strptime(break_start_time1,"%H:%M").time()
        # break_end_time1 = request.POST.get("break_end_time")
        # break_end_time = datetime.strptime(break_end_time1,"%H:%M").time()
        # if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
        #     messages.add_message(request,messages.ERROR,"At least select one day")
        #     return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id}))
        # if opening_time >= close_time or break_start_time >= close_time or break_end_time >= close_time or opening_time >= break_start_time  or opening_time >= break_end_time or break_start_time >= break_end_time:
        #     messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
        #     print(messages.error)
        #     return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id})) 

        # print("we are indside a add hspitals")
        try:
            # opd = OPDTime.objects.get(user=request.user)
            # opd.delete()
            # opdtime= OPDTime(user=request.user,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            # opdtime.save()
            hospital = Hospitals.objects.get(admin=request.user.id)
            hospital.hopital_name=hopital_name
            hospital.about=about
            hospital.registration_number=registration_number
            hospital.address1=address1
            hospital.address2=address2
            hospital.city=city
            hospital.pin_code=pin_code
            hospital.state=state
            hospital.country=country
            hospital.landline=landline
            if specialist:
                specialist1 = get_object_or_404(Specailist,id=specialist)
                hospital.specialist=specialist1

            if profile_pic:
                hospital.profile_pic=profile_pic
                hospital.admin.profile_pic=profile_pic

            print(registration_proof)
            if registration_proof:
                hospital.registration_proof=registration_proof
                
            hospital.establishment_year=establishment_year
            hospital.alternate_mobile=alternate_mobile
            hospital.website=website
            hospital.linkedin=linkedin
            hospital.facebook=facebook
            hospital.instagram=instagram
            hospital.twitter=twitter
            hospital.is_appiled=True
            hospital.is_verified=False
            hospital.firm=firm
            hospital.save()
            #edit customUSer
            hospital.admin.first_name=first_name
            hospital.admin.last_name=last_name
            hospital.admin.name_title=name_title       
            
            hospital.admin.save()
            
            k=0
            for insurance_name in insurance_name_list:
                insurance_id = insurances_id[k]
                if insurance_id == "blank" and insurance_name != "" : 
                    insurance =Insurances(hospital=hospital,insurance_type=insurance_type_list[k],insurance_name=insurance_name)
                    insurance.is_active =True
                    insurance.save()
                else:
                    if insurance_name != "":
                        insurance = Insurances.objects.get(id=insurance_id)
                        insurance.insurance_type = insurance_type_list[k]
                        insurance.insurance_name = insurance_name
                        insurance.save()

                k=k+1
            print("insurance saved") 

            j=0
            hos_mobiles = HospitalPhones.objects.filter(is_active=True) 
            for hospital_mobile in hospital_mobile_list:
                print(hospital_mobile_list)
                contact_id = contacts_id[j]
                if contact_id == "blank" and (hospital_mobile != "" or hospital_email_list[j] != ""):
                    if hos_mobiles:
                        for hos_mobile in hos_mobiles:
                            if hospital_mobile == hos_mobile.hospital_mobile or hospital_email_list[j] == hos_mobile.hospital_email :
                                messages.add_message(request,messages.ERROR," Mobile number or email id is already exist")                    
                    print("totol blank hai for hos_mobile is newly created !")
                    hospitalphone =HospitalPhones(hospital=hospital,hospital_mobile=hospital_mobile,hospital_email=hospital_email_list[j])
                    hospitalphone.is_active =True
                    hospitalphone.save()
                else:
                    if hospital_mobile != "" or hospital_email_list[j] != "" :
                        print("update phone number and wemail id !")
                        hospitalphone = HospitalPhones.objects.get(id=contact_id)
                        hospitalphone.hospital_mobile = hospital_mobile
                        hospitalphone.hospital_email = hospital_email_list[j]
                        hospitalphone.save()
                j=j+1

            print("phone saved")

                
            
            print("All data saved")

           
            # except:
            #     return render(request,"radmin/hospital_add.html") 
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)

        messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
        return HttpResponseRedirect(reverse("hospital_dashboard"))
 
def AcceptAPT(request,id):
    try:
        apt = get_object_or_404(OrderBooking,id=id,is_cancelled=False,is_active=True)
        is_applied = False        
        is_accepted = True
        status = "OTP_SEND"
        
        showtime = datetime.now(tz=IST)
        apt.accepted_date = showtime
        apt.status=status        
        apt.is_accepted=is_accepted    
        apt.is_applied=is_applied
        apt.save()  
        notification =  Notification(notification_type="1",from_user= request.user,to_user=apt.patient,booking=apt)
        notification.save()

        messages.add_message(request,messages.SUCCESS,"Appointment is Accepted")
    except Exception as e:
        messages.add_message(request,messages.ERROR,"Error in connection Try after sometimes")
    return HttpResponseRedirect(reverse("hospital_dashboard"))

def AcceptOTP(request,id):
    apt = get_object_or_404(OrderBooking,id=id,is_cancelled=False,is_active=True)
    phoneotp = get_object_or_404(phoneOPTforoders, order_id = apt)
    user = phoneotp.user #mobile is a user     
    key = phoneotp.otp  # Generating Key      
    postotp=request.POST.get("otp")
    # next_date=request.POST.get("next_date")
    try:
             
        is_accepted = False
        is_otp_verified =True
        is_taken =True
        status = "TAKEN"
         
        showtime = datetime.now(tz=IST)
        
        if postotp == str(key):  # Verifying the OTP
            apt.otp_verified_datetime = showtime
            apt.taken_date = showtime
            apt.status=status        
            apt.is_accepted=is_accepted    
            apt.is_otp_verified=is_otp_verified
            apt.is_taken=is_taken
            apt.save() 

            phoneotp.validated = True          
            phoneotp.save()    
            
            treatmentreliefpetient = TreatmentReliefPetient(patient=apt.patient.patients,booking=apt,status="CHECKEDUP",amount_paid=apt.amount,is_active=True)
            # treatmentreliefpetient.next_date=next_date
            treatmentreliefpetient.save()

            notification =  Notification(notification_type="1",from_user= request.user,to_user=apt.patient,booking=apt)
            notification.save()
            print(notification)
            messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
        else:
            messages.add_message(request,messages.ERROR,"OTP does not matched")
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
    return HttpResponseRedirect(reverse("hospital_dashboard"))

def RejectedAPT(request,id):
    try:
        apt = get_object_or_404(OrderBooking,id=id,is_cancelled=False,is_active=True)       
        is_applied = False        
        is_accepted = False
        is_otp_verified =False
        is_taken =False
        is_rejected =True
        status = "REJECTED"
        
        showtime = datetime.now(tz=IST)
        apt.accepted_date = showtime
        apt.status=status        
        apt.is_accepted=is_accepted    
        apt.is_applied=is_applied
        apt.is_otp_verified=is_otp_verified
        apt.is_taken=is_taken
        apt.is_rejected=is_rejected
        apt.save()  
        notification =  Notification(notification_type="1",from_user= request.user,to_user=apt.patient,booking=apt)
        notification.save()

        messages.add_message(request,messages.SUCCESS,"Appointment is Rejected")
    except Exception as e:
        messages.add_message(request,messages.ERROR,"Error in connection Try after sometimes")
    return HttpResponseRedirect(reverse("hospital_dashboard"))

class hospitalUpdateViews(SuccessMessageMixin,UpdateView):
    UserModel=get_user_model()
    def get(self, request, *args, **kwargs):
        hospital = None
        # contacts = None
        # insurances = None
        try:
            hospital = Hospitals.objects.get(admin=request.user.id)
            contacts = HospitalPhones.objects.filter(hospital=hospital)
            insurances = Insurances.objects.filter(hospital=hospital)
            opdtime=OPDTime.objects.get(user=request.user)
            specailists = Specailist.objects.all()
        except Exception as e:
            return HttpResponse(e)
        param={'hospital':hospital,'insurances':insurances,'contacts':contacts,'opdtime':opdtime,'specailists':specailists}
        return render(request,"hospital/doctor-profile-settings.html",param) 
    
    def post(self, request, *args, **kwargs):
        hopital_name = request.POST.get("hopital_name")
        specialist = request.POST.get("specialist")
        profile_pic = request.FILES.get("profile_pic")

        firm = request.POST.get("firm")
        about = request.POST.get("about")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        pin_code = request.POST.get("pin_code")
        state = "Gujarat"
        country = "India"
        landline = request.POST.get("landline")
        establishment_year = request.POST.get("establishment_year")
        registration_number = request.POST.get("registration_number")
        registration_proof = request.FILES.get("registration_proof")
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        twitter = request.POST.get("twitter")
        website = request.POST.get("website")
        #contact detail
        hospital_mobile_list= request.POST.getlist("hospital_mobile[]")
        hospital_email_list = request.POST.getlist("hospital_email[]")
        #insuarance
        insurance_type_list = request.POST.getlist("insurance_type[]")
        insurance_name_list = request.POST.getlist("insurance_name[]")
        #hidden Ids from for loop
        insurances_id = request.POST.getlist("insurances_id[]")
        contacts_id = request.POST.getlist("contacts_id[]")
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        # Sunday = request.POST.get("Sunday")
        # Monday = request.POST.get("Monday")
        # Tuesday = request.POST.get("Tuesday")
        # Wednesday = request.POST.get("Wednesday")
        # Thursday = request.POST.get("Thursday")
        # Friday = request.POST.get("Friday")
        # Saturday = request.POST.get("Saturday")
        # Sunday = request.POST.get("Sunday")
        # opening_time1 = request.POST.get("opening_time")
        # opening_time = datetime.strptime(opening_time1,"%H:%M").time()
        # close_time1 = request.POST.get("close_time")
        # close_time = datetime.strptime(close_time1,"%H:%M").time()
        # break_start_time1 = request.POST.get("break_start_time")
        # break_start_time = datetime.strptime(break_start_time1,"%H:%M").time()
        # break_end_time1 = request.POST.get("break_end_time")
        # break_end_time = datetime.strptime(break_end_time1,"%H:%M").time()
        # if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
        #     messages.add_message(request,messages.ERROR,"At least select one day")
        #     return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id}))
        # if opening_time >= close_time or break_start_time >= close_time or break_end_time >= close_time or opening_time >= break_start_time  or opening_time >= break_end_time or break_start_time >= break_end_time:
        #     messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
        #     print(messages.error)
        #     return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id})) 

        # print("we are indside a add hspitals")
        # try:
            # opd = OPDTime.objects.get(user=request.user)
            # opd.delete()
            # opdtime= OPDTime(user=request.user,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            # opdtime.save()
        hospital = Hospitals.objects.get(admin=request.user.id)
        hospital.hopital_name=hopital_name
        hospital.about=about
        hospital.registration_number=registration_number
        hospital.address1=address1
        hospital.address2=address2
        hospital.city=city
        hospital.pin_code=pin_code
        hospital.state=state
        hospital.country=country
        hospital.landline=landline
        if specialist:
            specialist1 = get_object_or_404(Specailist,id=specialist)
            hospital.specialist=specialist1

        if profile_pic:
            hospital.profile_pic=profile_pic
            hospital.admin.profile_pic=profile_pic

        print(registration_proof)
        if registration_proof:
            hospital.registration_proof=registration_proof
            
        hospital.establishment_year=establishment_year
        hospital.alternate_mobile=alternate_mobile
        hospital.website=website
        hospital.linkedin=linkedin
        hospital.facebook=facebook
        hospital.instagram=instagram
        hospital.twitter=twitter
        hospital.is_appiled=True
        hospital.is_verified=False
        hospital.firm=firm
        hospital.save()
        #edit customUSer
        hospital.admin.first_name=first_name
        hospital.admin.last_name=last_name
        hospital.admin.name_title=name_title       
        print(profile_pic)
        hospital.admin.save()
        
        k=0
        for insurance_name in insurance_name_list:
            insurance_id = insurances_id[k]
            if insurance_id == "blank" and insurance_name != "" : 
                insurance =Insurances(hospital=hospital,insurance_type=insurance_type_list[k],insurance_name=insurance_name)
                insurance.is_active =True
                insurance.save()
            else:
                if insurance_name != "":
                    insurance = Insurances.objects.get(id=insurance_id)
                    insurance.insurance_type = insurance_type_list[k]
                    insurance.insurance_name = insurance_name
                    insurance.save()

            k=k+1
        print("insurance saved") 

        j=0
        hos_mobiles = HospitalPhones.objects.filter(is_active=True) 
        for hospital_mobile in hospital_mobile_list:
            print(hospital_mobile_list)
            contact_id = contacts_id[j]
            if contact_id == "blank" and (hospital_mobile != "" or hospital_email_list[j] != ""):
                if hos_mobiles:
                    for hos_mobile in hos_mobiles:
                        if hospital_mobile == hos_mobile.hospital_mobile or hospital_email_list[j] == hos_mobile.hospital_email :
                            messages.add_message(request,messages.ERROR," Mobile number or email id is already exist")                    
                print("totol blank hai for hos_mobile is newly created !")
                hospitalphone =HospitalPhones(hospital=hospital,hospital_mobile=hospital_mobile,hospital_email=hospital_email_list[j])
                hospitalphone.is_active =True
                hospitalphone.save()
            else:
                if hospital_mobile != "" or hospital_email_list[j] != "" :
                    print("update phone number and wemail id !")
                    hospitalphone = HospitalPhones.objects.get(id=contact_id)
                    hospitalphone.hospital_mobile = hospital_mobile
                    hospitalphone.hospital_email = hospital_email_list[j]
                    hospitalphone.save()
            j=j+1

        print("phone saved")

            
        
        print("All data saved")

           
            # except:
            #     return render(request,"radmin/hospital_add.html") 
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,e)

        messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
        return HttpResponseRedirect(reverse("hospital_update"))
#Try except done till here
class manageStaffView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            staffs = HospitalStaffs.objects.filter(hospital=hospital)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Hosptial not found")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'staffs':staffs}
        return render(request,"hospital/manage_staff.html",param)

    def post(self, request, *args, **kwargs):
        name_title = request.POST.get("name_title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        hospitalstaff = HospitalStaffs(hospital=hospital,name_title=name_title,first_name=first_name,last_name=last_name,email=email,mobile=mobile,is_active=active)
        hospitalstaff.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_staff"))

def updateStaff(request):
     if request.method == "POST":
        id= request.POST.get("id")
        name_title = request.POST.get("name_title")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospitalstaff = HospitalStaffs.objects.get(id=id)
        print(hospitalstaff)
        hospitalstaff.name_title=name_title
        hospitalstaff.first_name=first_name
        hospitalstaff.last_name=last_name
        hospitalstaff.email=email
        hospitalstaff.is_active=active
        hospitalstaff.save()
        print(hospitalstaff)
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_staff"))

def activeStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    if staff:
        staff.is_active=True        
        staff.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_staff"))

def deactiveStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    if staff:
        staff.is_active=False        
        staff.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_staff"))

def deleteHospitalStaff(request,id):
    staff = HospitalStaffs.objects.get(id=id)
    staff.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_staff"))

class manageDepartmentclassView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            staffs = HospitalStaffs.objects.filter(hospital=hospital)
            doctors = HospitalDoctors.objects.filter(hospital=hospital)
            departments = Departments.objects.filter(hospital=hospital)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'staffs':staffs,'departments':departments,'doctors':doctors}
        return render(request,"hospital/manage_deparment.html",param)

    def post(self, request, *args, **kwargs):
        department_name = request.POST.get("department_name")
        hospital_staff_doctor1 = request.POST.get("hospital_staff_doctor")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")
        if department_name == None or hospital_staff_doctor1 == None or mobile == None:
            messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
            return HttpResponseRedirect(reverse("manage_department"))
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        hospital_staff_doctor = HospitalDoctors.objects.get(id=hospital_staff_doctor1)
        hospitaldepartments = Departments(hospital=hospital,department_name=department_name,hospital_staff_doctor=hospital_staff_doctor,email=email,mobile=mobile,is_active=active)
        hospitaldepartments.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_department"))

def updateDepartment(request):
     if request.method == "POST":
        id= request.POST.get("id")
        department_name = request.POST.get("department_name")
        hospital_staff = request.POST.get("hospital_staff")
        email = request.POST.get("email")
        mobile = request.POST.get("phone")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospitalstaff1 = HospitalStaffs.objects.get(id=hospital_staff)
        hospitaldepartment = Departments.objects.get(id=id)
        hospitaldepartment.department_name=department_name
        hospitaldepartment.hospital_staff=hospitalstaff1
        hospitaldepartment.email=email
        hospitaldepartment.is_active=active
        hospitaldepartment.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_department"))

def activeDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    if hospitaldepartment:
        hospitaldepartment.is_active=True        
        hospitaldepartment.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_department"))

def deactiveDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    if hospitaldepartment:
        hospitaldepartment.is_active=False        
        hospitaldepartment.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_department"))

def deleteHospitalDepartment(request,id):
    hospitaldepartment = Departments.objects.get(id=id)
    hospitaldepartment.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_department"))

class manageRoomclassView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            roooOrbadtypeandrates = RoomOrBadTypeandRates.objects.filter(hospital=hospital)
            rooms = HospitalRooms.objects.filter(hospital=hospital)
            prices = RoomOrBadTypeandRates.objects.filter(hospital=hospital)
            # departments = Departments.objects.filter(hospital=hospital)
            # departments = Departments.objects.filter(hospital=hospital)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'rooms':rooms,'prices':prices}
        return render(request,"hospital/manage_room.html",param)

    def post(self, request, *args, **kwargs):
        floor = request.POST.get("floor")
        room_no = request.POST.get("room_no")
        room = request.POST.get("room")

        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=Hospitals.objects.get(admin=request.user)
        room_type = RoomOrBadTypeandRates.objects.get(id=room)
        hospitalroom = HospitalRooms(hospital=hospital,room=room_type,floor=floor,room_no=room_no,is_active=active)
        hospitalroom.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_room"))

def updateRoom(request ,id):
    if request.method == "POST":
        floor = request.POST.get("floor")
        room_no = request.POST.get("room_no")
        room = request.POST.get("room")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        room_type = RoomOrBadTypeandRates.objects.get(id=room)
        hospitalroom =get_object_or_404(HospitalRooms,id=id)
        hospitalroom.room=room_type
        hospitalroom.floor=floor
        hospitalroom.room_no=room_no
        hospitalroom.is_active=active
        hospitalroom.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_room"))

def activeRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    if hospitalroom:
        hospitalroom.is_active=True        
        hospitalroom.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_room"))

def deactiveRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    if hospitalroom:
        hospitalroom.is_active=False        
        hospitalroom.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_room"))
 
def deleteHospitalRoom(request,id):
    hospitalroom = HospitalRooms.objects.get(id=id)
    hospitalroom.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Deleted")
    return HttpResponseRedirect(reverse("manage_room"))

class manageAmbulanceclassView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        hospital=Hospitals.objects.get(admin=request.user)
        doctors = HospitalDoctors.objects.filter(hospital=hospital)
        ambulances = AmbulanceDetails.objects.filter(hospital=hospital)
        print("hello ambulance")
        param={'hospital':hospital,'ambulances':ambulances,'doctors':doctors}
        return render(request,"hospital/manage_ambulance.html",param)

    def post(self, request, *args, **kwargs):
        vehicle_number = request.POST.get("vehicle_number")
        drive_name = request.POST.get("drive_name")
        drive_number = request.POST.get("drive_number")
        charge = request.POST.get("charge")
        vehicle_type = request.POST.get("vehicle_type")
        doctor = request.POST.get("doctor")
        profile_pic = request.FILES.get("profile_pic")
        print(profile_pic)
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        hospital=get_object_or_404(Hospitals,admin=request.user)
        
        try:
            hospitalroom = AmbulanceDetails(hospital=hospital,vehicle_number=vehicle_number,drive_name=drive_name,drive_number=drive_number,charge=charge,vehicle_type=vehicle_type,is_active=active)
            if profile_pic: 
                hospitalroom.profile_pic=profile_pic
            if doctor:
                doctor =get_object_or_404(HospitalDoctors,id=doctor)
                hospitalroom.doctor=doctor
            hospitalroom.save()
        except:
            messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
            return HttpResponseRedirect(reverse("manage_ambulance"))
        return HttpResponseRedirect(reverse("manage_ambulance"))

def updateAmbulance(request):
    if request.method == "POST":
        id= request.POST.get("id")
        vehicle_number = request.POST.get("vehicle_number")
        drive_name = request.POST.get("drive_name")
        drive_number = request.POST.get("drive_number")
        charge = request.POST.get("charge")
        vehicle_type = request.POST.get("vehicle_type")
        is_active = request.POST.get("is_active")
        doctor = request.POST.get("doctor")
        profile_pic = request.FILES.get("profile_pic")

        active = False
        if is_active == "on":
            active= True
        try:
            hospital=get_object_or_404(Hospitals,admin=request.user)
            
            hospitalroom =get_object_or_404(AmbulanceDetails,id=id)
            hospitalroom.hospital=hospital
            hospitalroom.vehicle_number=vehicle_number
            hospitalroom.drive_name=drive_name
            hospitalroom.drive_number=drive_number
            hospitalroom.charge=charge
            hospitalroom.vehicle_type=vehicle_type
            hospitalroom.is_active=active
            if profile_pic:
                hospitalroom.profile_pic=profile_pic
            if doctor:
                doctor = get_object_or_404(HospitalDoctors,id=doctor)
                hospitalroom.doctor=doctor
            hospitalroom.save()
        except:
            messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
            return HttpResponseRedirect(reverse("manage_ambulance"))
        messages.add_message(request,messages.SUCCESS,"Successfully Updated")
        return HttpResponseRedirect(reverse("manage_ambulance"))

def deleteAmbulance(request,id):
    hospitalroom = AmbulanceDetails.objects.get(id=id)
    hospitalroom.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Deleted")
    return HttpResponseRedirect(reverse("manage_ambulance"))

def PriceCreate(request):
    if request.method == "POST":
        rooms_price = request.POST.get("rooms_price") 
        room_type = request.POST.get("room_type")
        is_active = request.POST.get("is_active")
        active = False
        if is_active == "on":
            active= True
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            roomorbadtypeandrate= RoomOrBadTypeandRates(hospital=hospital,room_type=room_type,rooms_price=rooms_price,is_active=active)
            roomorbadtypeandrate.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
        return HttpResponseRedirect(reverse("manage_room"))

def deletePrice(request,id):
    roomorbadtypeandrate = RoomOrBadTypeandRates.objects.get(id=id)
    roomorbadtypeandrate.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_room"))

"""Reviews list and edit delete """
class HospitalReviewsListView(SuccessMessageMixin,ListView):
     def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.filter(HLP = request.user)
            print(review_list)
            total_review = RatingAndComments.objects.filter(HLP = request.user).count()
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"hospital/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("hospitalreviews")) 

class manageDoctorView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try: 
            hospital=Hospitals.objects.get(admin=request.user)
            doctors = HospitalDoctors.objects.filter(hospital=hospital)
            is_virtual_available_check = HospitalDoctors.objects.filter(is_virtual_available=True,hospital=hospital,is_active=True).count()
            paginator = Paginator(doctors, 6) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            specailists = Specailist.objects.all() 
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_doctor"))        
        param={'hospital':hospital,'doctors':doctors,'is_virtual_available_check':is_virtual_available_check,'page_obj':page_obj,'specailists':specailists}
        return render(request,"hospital/new_manage_doctor.html",param)        

    def post(self, request, *args, **kwargs):
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        user_type = 3
        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count(): 
            messages.add_message(request,messages.ERROR,"Email Already Exits")     
            return HttpResponseRedirect(reverse("manage_doctor"))
            
        phone = request.POST.get('phone')
        p=CustomUser.objects.filter(phone=phone)
        if p.count():
            messages.add_message(request,messages.ERROR,"Phone Already Exits")
            return HttpResponseRedirect(reverse("manage_doctor"))
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        pin_code = request.POST.get("pin_code")
        degree = request.POST.get("degree")
        specialist_id = request.POST.get("specialist")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        opd_charges = request.POST.get("opd_charges")
        home_charges = request.POST.get("home_charges")
        online_charges = request.POST.get("online_charges")
        emergency_charges = request.POST.get("emergency_charges")
        is_active = request.POST.get("is_active")
        
        is_virtual = request.POST.get("is_virtual_available")
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
        is_homevisit = request.POST.get("is_homevisit_available")
        is_homevisit_available = False
        if is_homevisit == "Yes":
            is_homevisit_available = True
        print(is_virtual,is_virtual_available)
        print(is_homevisit,is_homevisit_available)
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        about = request.POST.get("about")
        hospital=Hospitals.objects.get(admin=request.user)

        account = CustomUser.objects.create_user(username=phone,password=phone,email=email)
        account.user_type=3
        account.phone=phone
        patient = HospitalDoctors()
        patient.admin = account
        patient.save()
        account.is_active = True
        account.is_Mobile_Verified = True
        account.save()
        if profile_pic:
            account.profile_pic=profile_pic
            account.hospitaldoctors.profile_pic=profile_pic    
        account.hospitaldoctors.fisrt_name=first_name
        account.hospitaldoctors.name_title="Dr."
        account.hospitaldoctors.last_name=last_name
        account.hospitaldoctors.address=address
        account.hospitaldoctors.city=city
        account.hospitaldoctors.state=state
        account.hospitaldoctors.country=country
        account.hospitaldoctors.pin_code=pin_code
        account.hospitaldoctors.phone=phone
        account.hospitaldoctors.degree=degree
        account.hospitaldoctors.dob=dob
        account.hospitaldoctors.alternate_mobile=alternate_mobile
        account.hospitaldoctors.profile_pic=profile_pic_url
        account.hospitaldoctors.gender=gender
        account.hospitaldoctors.facebook=facebook
        account.hospitaldoctors.instagram=instagram
        account.hospitaldoctors.linkedin=linkedin
        account.hospitaldoctors.about=about
        account.hospitaldoctors.is_appiled=False
        account.hospitaldoctors.is_virtual_available=is_virtual_available
        account.hospitaldoctors.is_homevisit_available=is_homevisit_available
        account.hospitaldoctors.is_verified=True
        account.hospitaldoctors.gender=gender
        account.hospitaldoctors.opd_charges=opd_charges
        account.hospitaldoctors.online_charges=online_charges
        account.hospitaldoctors.emergency_charges=emergency_charges
        account.hospitaldoctors.home_charges=home_charges
        account.hospitaldoctors.is_hospital_added=True
        account.hospitaldoctors.ssn_id=ssn_id
        account.hospitaldoctors.joindate=joindate
        account.hospitaldoctors.is_active=True
        account.hospitaldoctors.is_verified=True
        account.hospitaldoctors.hospital=hospital
        specialist = Specailist.objects.get(id=specialist_id)
        account.hospitaldoctors.specialist=specialist
        account.first_name = first_name
        account.last_name = last_name
        account.name_title = "Dr."
        account.save()
        account.hospitaldoctors.save()
       
        # staffdoctor= HospitalDoctors(doctor=account.hospitaldoctors,hospital=hospital,joindate=joindate,is_active=active,ssn_id=ssn_id,is_virtual_available=is_virtual_available,email=email,emergency_charges=emergency_charges,home_charges=home_charges,online_charges=online_charges,opd_charges=opd_charges)
        # staffdoctor.is_active=True
        # staffdoctor.save()
       
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_doctor"))

def updateDoctor(request):
     if request.method == "POST":
        id= request.POST.get("id")
        doctorid= request.POST.get("doctorid")
        print(doctorid,id)
        doctor=HospitalDoctors.objects.get(id=doctorid)
        print(doctor)
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        user_type = 3
        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)       
        # if e.count():
        #     if email != doctor.admin.email:
        #         messages.add_message(request,messages.ERROR,"Email Already Exits")     
        #         return HttpResponseRedirect(reverse("manage_doctor"))
            
        # phone = request.POST.get('phone')
        # p=CustomUser.objects.filter(phone=phone)
        # print(phone,doctor.admin.phone)     
        # if p.count():
        #     if phone != doctor.admin.phone:
        #         messages.add_message(request,messages.ERROR,"Phone Already Exits")
        #         return HttpResponseRedirect(reverse("manage_doctor"))
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        pin_code = request.POST.get("pin_code")
        degree = request.POST.get("degree")
        specialist_id = request.POST.get("specialist")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        opd_charges = request.POST.get("opd_charges")
        home_charges = request.POST.get("home_charges")
        online_charges = request.POST.get("online_charges")
        emergency_charges = request.POST.get("emergency_charges")
        is_active = request.POST.get("is_active")
        
        is_virtual = request.POST.get("is_virtual_available")
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
        is_homevisit = request.POST.get("is_homevisit_available")
        is_homevisit_available = False
        if is_homevisit == "Yes":
            is_homevisit_available = True
        print(is_virtual,is_virtual_available)
        print(is_homevisit,is_homevisit_available)
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        about = request.POST.get("about")

        hospital=Hospitals.objects.get(admin=request.user)
        

        if profile_pic:
            doctor.admin.profile_pic=profile_pic
            doctor.profile_pic=profile_pic    
        doctor.fisrt_name=first_name
        doctor.last_name=last_name
        doctor.address=address
        doctor.city=city
        doctor.state=state
        doctor.country=country
        doctor.pin_code=pin_code
        doctor.degree=degree
        doctor.dob=dob
        doctor.alternate_mobile=alternate_mobile
        doctor.gender=gender
        doctor.facebook=facebook
        doctor.instagram=instagram
        doctor.linkedin=linkedin
        doctor.about=about
        doctor.is_virtual_available=is_virtual_available
        doctor.is_homevisit_available=is_homevisit_available
        doctor.gender=gender
        doctor.opd_charges=opd_charges
        doctor.online_charges=online_charges
        doctor.emergency_charges=emergency_charges
        doctor.home_charges=home_charges
        doctor.is_hospital_added=True
        doctor.ssn_id=ssn_id
        doctor.joindate=joindate
        specialist = Specailist.objects.get(id=specialist_id)
        doctor.specialist=specialist
        doctor.admin.first_name = first_name
        doctor.admin.last_name = last_name
        doctor.admin.name_title = "Dr."
        doctor.admin.save()
        doctor.save()
        return HttpResponseRedirect(reverse("manage_doctor"))

def activeDoctor(request,id):
    doctor = HospitalDoctors.objects.get(id=id)
    if doctor:
        doctor.is_active=True        
        doctor.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_doctor"))

def deactiveDoctor(request,id):
    doctor = HospitalDoctors.objects.get(id=id)
    if doctor:
        doctor.is_active=False        
        doctor.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_doctor"))

def deleteHospitalDoctor(request,id):
    doctor = HospitalDoctors.objects.get(id=id)
    doctor.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_doctor"))

class manageDoctorSchedualView(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        id=kwargs["id"]
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            doctors = HospitalDoctors.objects.filter(hospital=hospital)
            hospitalstaffdoctor = HospitalDoctors.objects.get(id=id)
            
            hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'doctors':doctors,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual}
        return render(request,"hospital/doctor_schedule.html",param)        

    def post(self, request, *args, **kwargs):
        #for CustomUSer creation
        id=kwargs["id"]
        Sunday = request.POST.get("Sunday")
        Monday = request.POST.get("Monday")
        Tuesday = request.POST.get("Tuesday")
        Wednesday = request.POST.get("Wednesday")
        Thursday = request.POST.get("Thursday")
        Friday = request.POST.get("Friday")
        Saturday = request.POST.get("Saturday")
        Sunday = request.POST.get("Sunday")
        opd_duration = request.POST.get("opd_duration")
        work = request.POST.get("work")
        start_time1 = request.POST.get("start_time")
        start_time = None
        if start_time1 and start_time1 != None:
            start_time = datetime.strptime(start_time1,"%H:%M").time()
        break_time_start1 = request.POST.get("break_time_start")
        break_time_start = None
        if break_time_start1 and break_time_start1 != None:
            break_time_start = datetime.strptime(break_time_start1,"%H:%M").time()
        break_time_end1 = request.POST.get("break_time_end")
        break_time_end = None
        if break_time_end1 and break_time_end1 != None:
            break_time_end = datetime.strptime(break_time_end1,"%H:%M").time()
        end_time1 = request.POST.get("end_time")
        end_time = None
        if end_time1 and end_time1 != None:
            end_time = datetime.strptime(end_time1,"%H:%M").time()
        print("1 one")
        if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
            messages.add_message(request,messages.ERROR,"At least select one day")
            print("these all none")
            return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
        if break_time_start != None or break_time_end != None:
            if start_time >= end_time or break_time_start >= end_time or break_time_end >= end_time or start_time >= break_time_start  or start_time >= break_time_end or break_time_start >= break_time_end:
                messages.add_message(request,messages.ERROR,"Time Does not match please arrang eproper timing ")
                return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
        elif start_time >= end_time:
            messages.add_message(request,messages.ERROR,"Time Does not match please arrang eproper timing ")
            return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id})) 
        print("2")
        # hsds = HospitalStaffDoctorSchedual.objects.filter(id=id and (Q(sunday = Sunday) | Q(monday=Monday) | Q(tuesday=Tuesday)| Q(wednesday = Wednesday) | Q(thursday=Thursday) | Q(friday=Friday)| Q(saturday=Saturday)) )      hospitalstaffdoctor_id
        hsds = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor_id=id)
        print(hsds)
        for hsd in hsds:
            if hsd.sunday == Sunday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))  
            if hsd.monday == Monday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
            if hsd.tuesday == Tuesday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
            if hsd.wednesday == Wednesday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
            if hsd.thursday == Thursday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
            if hsd.friday == Friday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))
            if hsd.saturday == Saturday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))

        hospitalstaffdoctor = HospitalDoctors.objects.get(id=id)
        hospital=Hospitals.objects.get(admin=request.user)
        # for day in days:
        hospitalstaffdoctorschedual= HospitalStaffDoctorSchedual(hospital=hospital,hospitalstaffdoctor=hospitalstaffdoctor,end_time=end_time,work=work,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,start_time=start_time,break_time_start=break_time_start,break_time_end=break_time_end,opd_duration=int(opd_duration))
        hospitalstaffdoctorschedual.save()
       
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':id}))

def updateDoctorSchedual(request ,id,sid):
    if request.method == "POST":
        # sid = request.POST.get("sid")
        Sunday = request.POST.get("Sunday")
        Monday = request.POST.get("Monday")
        Tuesday = request.POST.get("Tuesday")
        Wednesday = request.POST.get("Wednesday")
        Thursday = request.POST.get("Thursday")
        Friday = request.POST.get("Friday")
        Saturday = request.POST.get("Saturday")
        Sunday = request.POST.get("Sunday")
        opd_duration = request.POST.get("opd_duration")
        work = request.POST.get("work")
        break_time_start1 = request.POST.get("break_time_start")
        break_time_start = datetime.strptime(break_time_start1,"%H:%M").time()
        break_time_end1 = request.POST.get("break_time_end")
        break_time_end = datetime.strptime(break_time_end1,"%H:%M").time()
        start_time1 = request.POST.get("start_time")
        start_time = datetime.strptime(start_time1,"%H:%M").time()
        end_time1 = request.POST.get("end_time")
        end_time = datetime.strptime(end_time1,"%H:%M").time()
       

        if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
            messages.add_message(request,messages.ERROR,"At least select one day")
            print("these all none")
            return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
        if start_time >= end_time or break_time_start >= end_time or break_time_end >= end_time or start_time >= break_time_start  or start_time >= break_time_end or break_time_start >= break_time_end:
            messages.add_message(request,messages.ERROR,"Time does not match")
            print(messages.error)
            return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid})) 
        deletehsds = HospitalStaffDoctorSchedual.objects.get(id=id)
        deletehsds.delete()
        hospitalstaffdoctor = HospitalDoctors.objects.get(id=sid)
        print(hospitalstaffdoctor)
        hospital=Hospitals.objects.get(admin=request.user)
        hsds = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor = hospitalstaffdoctor)
        print(hsds)
        print("1")
        for hsd in hsds:
            if hsd.sunday == Sunday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR," sunday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))  
            if hsd.monday == Monday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR," monday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
            if hsd.tuesday == Tuesday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR," tuesday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
            if hsd.wednesday == Wednesday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR," wednesday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
            if hsd.thursday == Thursday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"thursday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
            if hsd.friday == Friday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR,"friday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))
            if hsd.saturday == Saturday:
                if hsd.start_time <= start_time  and start_time <= hsd.end_time or hsd.start_time <= end_time  and end_time <= hsd.end_time :
                    messages.add_message(request,messages.ERROR," SAturday Already time slot booked")
                    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))       
        
        print("hello")
        hospitalstaffdoctorschedual= HospitalStaffDoctorSchedual(hospital=hospital,hospitalstaffdoctor=hospitalstaffdoctor,end_time=end_time,work=work,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,start_time=start_time,break_time_start=break_time_start,break_time_end=break_time_end,opd_duration=int(opd_duration))
        hospitalstaffdoctorschedual.save()
        # except:
        #     messages.add_message(request,messages.ERROR,"Connection Error Try after some time")
        #     return HttpResponseRedirect(reverse("manage_staff"))
        return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))

def deleteHospitalDoctorschedual(request,id,sid):
    doctor = HospitalStaffDoctorSchedual.objects.get(id=id)
    doctor.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_doctorschedule", kwargs={'id':sid}))

class manageGalleryView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            hospitalmedias = HospitalMedias.objects.filter(hospital=hospital)
            paginator = Paginator(hospitalmedias, 3) # Show 25 contacts per page.
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_staff"))        
        param={'hospital':hospital,'hospitalmedias':hospitalmedias,'page_obj':page_obj}
        return render(request,"hospital/new_manage_gallery.html",param)        

    def post(self, request, *args, **kwargs):
        media_type_list = request.POST.get('media_type')        
        media_content_list = request.FILES.getlist('media_content[]')        
        media_desc_list = request.POST.get('media_desc') 
        hospital=Hospitals.objects.get(admin=request.user)
        
        i=0
        for media_content in media_content_list:
            hospital_media = HospitalMedias(hospital=hospital,media_type=media_type_list,media_desc=media_desc_list,media_content=media_content)
            hospital_media.is_active=True
            hospital_media.save() 
            i=i+1  
            print("Meida saved")      
        return HttpResponseRedirect(reverse("manage_gallery"))

def deleteGallery(request,id):
    # if request.method == "POST":
        # checked = request.POST.get("id")
        # print(checked_list)
        # for deletecheck in checked_list:
    hospital_media = HospitalMedias.objects.get(id=id)
    hospital_media.delete()
    messages.add_message(request,messages.SUCCESS,"Successfully gellery Deleted")
    return HttpResponseRedirect(reverse("manage_gallery"))
 
"""
Patient creations just for hosiptal visit patients but for backend i and adding patient cardential
"""
class managePatientView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            hos_patients = Patients.objects.filter(hospital=hospital,is_active=True)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_patient"))        
        param={'hospital':hospital,'hos_patients':hos_patients}
        return render(request,"hospital/manage_patient.html",param)        

    def post(self, request, *args, **kwargs):
        #for CustomUSer creation
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        treatment = request.POST.get("treatment")
        age = request.POST.get("age")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        email = request.POST.get("email")
        add_notes = request.POST.get("add_notes")
        phone = request.POST.get("phone")
        ID_number = request.POST.get("ID_number")
        status = request.POST.get("status")
        ID_proof = request.FILES.get("ID_proof")
        profile_pic = request.FILES.get("profile_pic")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pin_code = request.POST.get("pin_code")
        gender = request.POST.get("gender")
        country = request.POST.get("country")
        blood_docation_date = request.POST.get("blood_docation_date")
        bloodgroup = request.POST.get("bloodgroup")
        # for Hospital staff user creation

        if ID_proof:
            ID_proof_url = ID_proof
        p=CustomUser.objects.filter(phone=phone).count()
        e=CustomUser.objects.filter(email=email).count()
        if p > 0:
            msg=messages.error(request,"Phone Already Exits")
            return HttpResponseRedirect(reverse("manage_patient"))        
        if e > 0:
            msg=messages.error(request,"Email Already Exits")
            return HttpResponseRedirect(reverse("manage_patient"))        
       
        hospital=Hospitals.objects.get(admin=request.user)

        
        """
        here i m adding admin as request.user means as a hospital 
        I Assuming this will only work for patient 
        """

        account = CustomUser.objects.create_user(username=phone,password=phone,email=email)
        account.user_type=4
        account.phone=phone
        patient = Patients()
        patient.admin = account
        patient.save()
        account.is_active = True
        account.save()
        if profile_pic:
            account.profile_pic=profile_pic
            account.patients.profile_pic=profile_pic        
        account.name_title = name_title
        account.first_name = first_name
        account.last_name = last_name
        account.patients.fisrt_name = first_name
        account.patients.last_name = last_name
        account.patients.address = address 
        account.patients.city = city 
        account.patients.state = state
        account.patients.country = country 
        account.patients.pin_code = pin_code  
        account.patients.dob = dob 
        account.patients.age = age 
        account.patients.alternate_mobile = alternate_mobile
        account.patients.profile_pic = profile_pic
        account.patients.gender = gender
        account.patients.bloodgroup = bloodgroup
        account.patients.hospital = hospital
        account.patients.status = status
      
        account.patients.added_by_hospital = True 
        account.patients.is_active = True 
        account.patients.save()   
        account.save()
       
        messages.add_message(request,messages.SUCCESS,"Successfully Added")
        return HttpResponseRedirect(reverse("manage_patient"))

def updatePatientView(request):
    if request.method == "POST":
        #for CustomUSer creation
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        treatment = request.POST.get("treatment")
        age = request.POST.get("age")
        email = request.POST.get("email")
        add_notes = request.POST.get("add_notes")
        phone = request.POST.get("phone")
        ID_number = request.POST.get("ID_number")
        status = request.POST.get("status")
        ID_proof = request.FILES.get("ID_proof")
        address = request.POST.get("address")
        city = request.POST.get("city")
        gender = request.POST.get("gender")
        id = request.POST.get("id")
        state = request.POST.get("state")
        pin_code = request.POST.get("pin_code")
        gender = request.POST.get("gender")
        bloodgroup = request.POST.get("bloodgroup")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        profile_pic = request.FILES.get("profile_pic")
        # for Hospital staff user creation

       
           
        hospital=Hospitals.objects.get(admin=request.user)     
        """
       Updating Hospital Patient for now
        """
        

        patient = HospitalsPatients(id=id,hospital=hospital)
        patient.name_title=name_title
        patient.first_name=first_name
        patient.last_name=last_name
        patient.address=address
        patient.city=city
        patient.age=age
        patient.phone=phone
        patient.treatment=treatment
        patient.ID_number=ID_number
        patient.status=status
        if ID_proof:
            profile_pic_url = ID_proof
        patient.ID_proof=profile_pic_url
        patient.add_notes=add_notes
        patient.gender=gender
        patient.is_active=True
        patient.email=email        
        patient.save()
       
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
        return HttpResponseRedirect(reverse("manage_patient"))

def deleteHospitalPatient(request,id):
    hospital=Hospitals.objects.get(admin=request.user)  
    patient = Patients.objects.get(id=id,hospital=hospital)
    patient.is_active=False
    patient.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_patient"))

class managePricesView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=get_object_or_404(Hospitals,admin=request.user)
            services = ServiceAndCharges.objects.filter(user=request.user,is_active=True)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_price"))        
        param={'hospital':hospital,'services':services}
        return render(request,"hospital/service_and_prices.html",param)        

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            service_name = request.POST.get("service_name")
            service_charge = request.POST.get("service_charge")
            hospital=get_object_or_404(Hospitals,admin=request.user)

            service = ServiceAndCharges(user=request.user,service_name=service_name,service_charge=service_charge,is_active =True)
            service.save()
            messages.add_message(request,messages.SUCCESS,"Successfully Added")     
        return HttpResponseRedirect(reverse("manage_price"))

def updateServicePrice(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        id = request.POST.get("id")
        service_charge = request.POST.get("service_charge")
        hospital=get_object_or_404(Hospitals,admin=request.user)  
        service =get_object_or_404(ServiceAndCharges,id=id,user=request.user)
        service.service_name=service_name
        service.service_charge=service_charge
        service.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
    return HttpResponseRedirect(reverse("manage_price"))

def deleteServicePrice(request,id):
    service = service =get_object_or_404(ServiceAndCharges,id=id)
    service.is_active = False
    service.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_price"))

class manageAppointmentView(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            booking = Booking.objects.filter(service__user=hospital.admin,is_active=True,is_cancelled = False,is_taken=False)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_appoinment"))        
        param={'hospital':hospital,'booking':booking}
        return render(request,"hospital/manage_appointment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
        is_accepted = False
        is_taken = False
        is_rejected =False
        is_applied = False        
        try:
            booking = Booking.objects.get(id=id)
            showtime = datetime.now(tz=IST)
            print(status)
        
            if status == 'accepted':
                is_accepted = True
                booking.accepted_date= showtime                
            elif status == 'rejected':
                is_rejected = True
                booking.rejected_date= showtime
            else:
                is_applied =True
            booking.is_accepted=is_accepted
            booking.is_rejected=is_rejected
            booking.is_taken=is_taken
            booking.status=status        
            booking.is_applied=is_applied
            booking.save() 
            print(booking)
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,booking=booking)
            notification.save()
            print(notification)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(e)

def verifybooking(request):
    if request.POST:
        # try:
        id = request.POST.get("booking_id")
        booking = Booking.objects.get(id=id)
        order = get_object_or_404(Orders,booking_for=1,bookingandlabtest=id)
        phoneotp = get_object_or_404(phoneOPTforoders, order_id = order)
        user = phoneotp.user #mobile is a user     
    
        postotp=request.POST.get("otp")
        
        showtime = datetime.now(tz=IST)
        key = phoneotp.otp  # Generating Key
        if postotp == str(key):  # Verifying the OTP
            order.is_booking_Verified = True
            order.save()
            phoneotp.validated = True          
            phoneotp.save()
            is_taken= True
            booking.is_taken=is_taken
            booking.status="taken"        
            booking.taken_date= showtime
            booking.save()
            
            treatmentreliefpetient = TreatmentReliefPetient(patient=booking.patient.patients,booking=booking,status="CHECKUPED",amount_paid=booking.service.service_charge,is_active=True)
            treatmentreliefpetient.save()

            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,booking=booking)
            notification.save()
            print(notification)
            messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
        else:
            messages.add_message(request,messages.ERROR,"OTP does not matched")
        return HttpResponseRedirect(reverse("manage_appointment"))
            #emila message for email verification
            # current_site=get_current_site(request) #fetch domain    
            # email_subject='Confirmation email for you booking order',
            # message=render_to_string('accounts/activate.html',
            # {
            #     'user':user,
            #     'domain':current_site.domain,
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token':generate_token.make_token(user)
            # } #convert Link into string/message
            # )
            # print(message)
            # email_message=EmailMessage(
            #     email_subject,
            #     message,
            #     settings.EMAIL_HOST_USER,
            #     [user.email]
            # )#compose email
            # print(email_message)
            # email_message.send() #send Email
            # messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")  
           
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,e)
        #     return HttpResponse(e)  # False Call    
        
"""
Update appointment yet not implemented will think more that
"""
# def updateAppointment(request):
#     if request.method == "POST":
#         id = request.POST.get("id")
#         modified_date = request.POST.get("modified_date")
#         modified_time = request.POST.get("modified_time")
#         add_note = request.POST.get("add_note")
#         booking = Booking.objects.get(id=id) 
#         booking.modified_date = modified_date
#         booking.modified_time = modified_time
#         booking.add_note = add_note
#         booking.save()
#         messages.add_message(request,messages.SUCCESS,"Appointment Successfully Update")
#         return HttpResponseRedirect(reverse("manage_appointment"))

def dateleAppointment(request, id):
    booking = Booking.objects.get(id=id)
    booking.is_active = False
    booking.save()
    messages.add_message(request,messages.SUCCESS,"Appointment Successfully Deleted")
    return HttpResponseRedirect(reverse("manage_appointment"))

class manageTreatmentViews(SuccessMessageMixin,DetailView):
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            hospital=Hospitals.objects.get(admin=request.user)
            treatmentreliefpetient = TreatmentReliefPetient.objects.get(is_active=True,id=id)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_relief_patient"))        
        param={'hospital':hospital,'treatmentreliefpetient':treatmentreliefpetient}
        return render(request,"hospital/manage_treatment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
           
        try:
            pass
        except Exception as e:
            print(e)
            # return HttpResponse(e)
       
        print("Appoinment update saved")      
        return HttpResponseRedirect(reverse("manage_treatment"))

class ReliefPatientViewsProfile(SuccessMessageMixin,DetailView):
     def get(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            hospital=Hospitals.objects.get(admin=request.user)
            treatmentreliefpetient = TreatmentReliefPetient.objects.get(is_active=True,id=id)
            oldbooking = TreatmentReliefPetient.objects.filter(is_active=True,patient=treatmentreliefpetient.patient)
            hospitaldoctors = HospitalDoctors.objects.filter(hospital=hospital,is_active=True)
            serviceandcharges = ServiceAndCharges.objects.filter(user=hospital.admin)
            patientfiles = patientFile.objects.filter(treatmentreliefpetient=treatmentreliefpetient) 
            slot = Slot.objects.filter(patient=treatmentreliefpetient.patient.admin) # yet not required
            labtests =LabTest.objects.filter(slot__patient=treatmentreliefpetient.patient.admin,is_active=True,slot__send_to_doctor=True)
            print(labtests)
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("manage_relief_patient"))        
        param={'hospital':hospital,'treatmentreliefpetient':treatmentreliefpetient,'oldbooking':oldbooking,'hospitaldoctors':hospitaldoctors,'serviceandcharges':serviceandcharges,'patientfiles':patientfiles,'labtests':labtests}
        return render(request,"hospital/patient_profile.html",param)        
 
def ReliefPatientViewsFiles(request,id):
    if request.method == "POST":
        file = request.FILES.get("file")
        # file_purpose = request.POST.get("file_purpose")
        # file_date = request.POST.get("file_date")
        # file_time = request.POST.get("file_time")
        file_addnote = request.POST.get("file_addnote")
        next_date = request.POST.get("next_date")
        print(id,file,file_addnote,next_date)
        is_active= True
        treatmentreliefpetient =get_object_or_404(TreatmentReliefPetient,id=id)
        
        try:
            patientfile = patientFile(treatmentreliefpetient=treatmentreliefpetient,patient=treatmentreliefpetient.patient,booking=treatmentreliefpetient.booking ,hospitaldoctors=treatmentreliefpetient.booking.hospitalstaffdoctor,file_addnote=file_addnote,is_active=is_active)
            if file:
                patientfile.file=file
            patientfile.save()
            treatmentreliefpetient.next_date=next_date
            treatmentreliefpetient.save()
            return HttpResponseRedirect(reverse("relief_patient_profile",kwargs={'id':treatmentreliefpetient.id}))
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("relief_patient_profile",kwargs={'id':treatmentreliefpetient.id}))
    
class manageReliefPatientViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try:
            hospital=Hospitals.objects.get(admin=request.user)
            treatmentreliefpetient = TreatmentReliefPetient.objects.filter(is_active=True,booking__is_taken=True,booking__hospitalstaffdoctor__hospital=hospital)
            print(treatmentreliefpetient)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_relief_patient"))        
        param={'hospital':hospital,'treatmentreliefpetient':treatmentreliefpetient}
        return render(request,"hospital/manage_relief_patient.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
           
        try:
            pass
        except Exception as e:
            print(e)
            # return HttpResponse(e)
       
        print("Appoinment update saved")      
        return HttpResponseRedirect(reverse("manage_relief_patient"))

def deleteReliefHospitalPatient(request,id):
    patient = TreatmentReliefPetient.objects.get(id=id)
    patient.is_active=False
    patient.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_relief_patient"))

""""New Doctor schedule"""

# class DoctorScheduleListView(SuccessMessageMixin,ListView):
#     def get(self, request, *args, **kwargs):
        
#         param={'hospital':hospital,'treatmentreliefpetient':treatmentreliefpetient}
#         return render(request,"hospital/view-doctor-schedule.html",param)        

#     # def post(self, request, *args, **kwargs):
#     #     id = request.POST.get('a_id')        
#     #     status = request.POST.get('status')
           
#     #     try:
#     #         pass
#     #     except Exception as e:
#     #         print(e)
#     #         # return HttpResponse(e)
       
#     #     print("Appoinment update saved")      
#     #     return HttpResponseRedirect(reverse("manage_relief_patient"))
#     # template_name = "hospital/view-doctor-schedule.html"
""""NEW DOCTORS SLOT IN BOX"""
class DoctorScheduleCreateView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        doctor_id = kwargs['id']
        doctor = get_object_or_404(HospitalDoctors,id=doctor_id)
        dates = DoctorSchedule.objects.filter(doctor=doctor).values('scheduleDate','id').order_by('-scheduleDate')
        schedule_dates ={item['scheduleDate'] for item in dates}
        schedule_dates_list = []
        for sch_Dat in schedule_dates:
            scd_type = DoctorSchedule.objects.filter(scheduleDate=sch_Dat,doctor=doctor).first()
            scd_type_all = DoctorSchedule.objects.filter(scheduleDate=sch_Dat,doctor=doctor).order_by('-scheduleDate')
            schedule_dates_list.append({'scd_type':scd_type,'sch_Dat':sch_Dat,'scd_type_all':scd_type_all})
            
            # sch_type = DoctorSchedule.objects.values('scheduleDate','id')


        # schedule_dates = DoctorSchedule.objects.filter()
        timeslots_15s = TimeSlot.objects.filter(schedule_type="15")
        timeslots_30s = TimeSlot.objects.filter(schedule_type="30")
        timeslots_45s = TimeSlot.objects.filter(schedule_type="45")
        timeslots_60s = TimeSlot.objects.filter(schedule_type="60")       
        
        param = {'timeslots_15s':timeslots_15s,'timeslots_30s':timeslots_30s,'timeslots_45s':timeslots_45s,'timeslots_60s':timeslots_60s,'doctor':doctor,'schedule_dates_list':schedule_dates_list}
       
        return render(request,'hospital/view-doctor-schedule.html',param)
    
    def post(self, request, *args, **kwargs):
        timeslot_list = request.POST.getlist('timeslot[]')
        scheduleDate = request.POST.get('scheduleDate')
        doctor_id = request.POST.get('doctor_id') 
        days = request.POST.get('days')

        doctor = get_object_or_404(HospitalDoctors,id=doctor_id)
        for x in range(int(days)):
            newdate = datetime.strptime(scheduleDate,"%Y-%m-%d") + timedelta(days=int(x))
            doctorschedules = DoctorSchedule.objects.filter(doctor = doctor)
            for doctorschedule in doctorschedules:
                print(doctorschedule.scheduleDate)
                print(newdate.date())
                if doctorschedule.scheduleDate == newdate.date():
                    messages.add_message(request,messages.ERROR,"Already Booked date please delete if you want to change")
                    return HttpResponseRedirect(reverse("manage_doctorschedule",kwargs={'id':doctor.id}))
            is_active =True
            for timeslot in timeslot_list:
                timeslot_obj = get_object_or_404(TimeSlot,id=timeslot)
                doctorschedule = DoctorSchedule(scheduleDate=newdate,doctor=doctor,is_active=is_active,timeslot=timeslot_obj,hospital=request.user.hospitals)
                doctorschedule.save()
        messages.add_message(request,messages.SUCCESS,"Suucessfully Created")
        return HttpResponseRedirect(reverse("manage_doctorschedule",kwargs={'id':doctor.id}))
 
def deleteTimeSlot(request,id,did):
    doctor = get_object_or_404(HospitalDoctors,id=did)
    date1 = DoctorSchedule.objects.get(doctor=doctor,id=id)
    dates = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date1.scheduleDate)
    for date in dates:
        date.delete()
    messages.add_message(request,messages.SUCCESS,"Sucessfully Deleted")
    return HttpResponseRedirect(reverse("manage_doctorschedule",kwargs={'id':doctor.id}))

""" Blog """

class addBlogView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):        
        blogs = Blog.objects.all()
        hospital=Hospitals.objects.get(admin=request.user) 
        doctors = HospitalDoctors.objects.filter(hospital=hospital)
        param={'blogs':blogs,'doctors':doctors}
        return render(request,"hospital/add-blog.html",param)  

    def post(self, request, *args, **kwargs):
        blog_title = request.POST.get('blog_title')         
        content = request.POST.get('content')
        blog_image = request.FILES.get('blog_image')
        doctor = request.POST.get('doctor')
        # try:
        hospital=Hospitals.objects.get(admin=request.user) 
        doctor = get_object_or_404(HospitalDoctors,id=doctor)
        blog = Blog(blog_title=blog_title,blog_content=content,hospital=hospital,doctor=doctor)
        if blog_image:
            blog.blog_image=blog_image
        blog.save()
        # except Exception as e:
            # messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            # return HttpResponseRedirect(reverse("add_blog"))
        return HttpResponseRedirect(reverse("list_blog"))
 
class EditBlogUpdateView(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        print("no error till here i am at editblogupdateview")
        id=kwargs['id']        
        blog =get_object_or_404(Blog,id=id)
        hospital=Hospitals.objects.get(admin=request.user) 
        doctors = HospitalDoctors.objects.filter(hospital=hospital)
        param={'blog':blog,'doctors':doctors}
        return render(request,"hospital/edit-blog.html",param)  
    
    def post(self, request, *args, **kwargs):
        id=kwargs['id']   
        blog_title = request.POST.get('blog_title')         
        content = request.POST.get('content')
        blog_image = request.FILES.get('blog_image')
        doctor = request.POST.get('doctor')
        # try:
        doctor = get_object_or_404(HospitalDoctors,id=doctor)
        blog =get_object_or_404(Blog,id=id)
        blog.blog_title=blog_title
        blog.blog_content=content
        blog.doctor=doctor
        if blog_image:
            blog.blog_image=blog_image
        blog.save()
        # except Exception as e:
            # messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            # return HttpResponseRedirect(reverse("add_blog"))
        return HttpResponseRedirect(reverse("list_blog"))

    def post(self, request, *args, **kwargs):
        id=kwargs['id']
        blog_title = request.POST.get('blog_title')         
        content = request.POST.get('content')
        blog_image = request.FILES.get('blog_image')
        doctor = request.POST.get('doctor')
        try:
            hospital=Hospitals.objects.get(admin=request.user) 
            doctor = get_object_or_404(HospitalDoctors,id=doctor)
            blog = get_object_or_404(Blog,id=id)
            blog.blog_title=blog_title
            blog.blog_content=content
            if blog_image:
                blog.blog_image=blog_image
            blog.hospital=hospital
            blog.doctor=doctor
            blog.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            return HttpResponseRedirect(reverse("add_blog"))
        return HttpResponseRedirect(reverse("list_blog"))
 
def activeBlog(request,id): 
    blog = get_object_or_404(Blog,id=id)
    blog.is_active=True        
    blog.save()
    messages.add_message(request,messages.SUCCESS,"Successfull Active")
    return HttpResponseRedirect(reverse("list_blog"))

def inactiveBlog(request,id):
    blog = get_object_or_404(Blog,id=id)
    blog.is_active=False        
    blog.save()
    messages.add_message(request,messages.SUCCESS,"Successfull Inactive")
    return HttpResponseRedirect(reverse("list_blog"))

class blogListView(ListView):
    model = Blog
    template_name = "hospital/blog.html"

class ReviewsList(ListView):
    model = RatingAndComments 
    template_name = "hospital/reviews.html" 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["reviews"] = RatingAndComments.objects.filter(HLP = self.request.user) 
        total_cmns = RatingAndComments.objects.filter(HLP = self.request.user).count()
        cmnss = RatingAndComments.objects.filter(HLP = self.request.user)
        rating = 0 
        for cmn in cmnss:
            rating = rating + cmn.rating
        if total_cmns > 0: 
            rating = rating / total_cmns
        context["total_reviews"] = total_cmns
        return context

"""Manage Disease Add and Update Listout"""
class manageDiseaseView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):  
        hospital = get_object_or_404(Hospitals,admin=request.user)        
        hos_diseases = HospitalDisease.objects.filter(hospital=hospital)
        diseases = Disease.objects.filter(is_active=True)
        param={'diseases':diseases,'hos_diseases':hos_diseases}
        return render(request,"hospital/add-disease.html",param)  

    def post(self, request, *args, **kwargs):
        name_list = request.POST.getlist('name []') 
        try:
            hospital = get_object_or_404(Hospitals,admin=request.user)
            hos_des_dl = HospitalDisease.objects.filter(hospital=hospital)
            for hos in hos_des_dl:
                hos.delete()      
            for name in name_list:
                ds = get_object_or_404(Disease,id=name)
                hospitaldiseas = HospitalDisease(hospital=hospital,disease = ds)
                hospitaldiseas.save()
            messages.add_message(request,messages.SUCCESS,"Successfully Added")
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            return HttpResponseRedirect(reverse("add_blog"))
        return HttpResponseRedirect(reverse("manage_disease"))

