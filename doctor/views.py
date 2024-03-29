from io import StringIO
from re import escape
from typing import List
from django.contrib.auth.models import User
from django.http import request
from django.http.request import HttpRequest
from accounts import models
import accounts
from chat.models import Notification
from front.models import RatingAndComments
from patient.models import Booking, LabTest, OrderBooking, Orders, Slot, TreatmentReliefPetient, patientFile, phoneOPTforoders
from django.db.models.query_utils import Q
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
from accounts.models import CustomUser,HospitalDoctors, HospitalPhones, Hospitals, OPDTime, Patients, Specailist
from django.urls import reverse
from datetime import datetime, timedelta
import pytz
from django.core.paginator import Paginator

from radmin.models import Disease, HospitalDisease
IST = pytz.timezone('Asia/Kolkata')

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

class doctordDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        # try: 
        # deactivating all old appoinments
        doctor = HospitalDoctors.objects.get(admin=request.user.id)
        showdate = datetime.now(tz=IST).date()
        showtime = datetime.now(tz=IST).time()
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
       
        if doctor.hospital:
            bookings = OrderBooking.objects.filter(hospitalstaffdoctor=doctor,HLP=doctor.hospital.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,is_rejected = False).order_by('applied_time')

            upcoming_bookings = OrderBooking.objects.filter(hospitalstaffdoctor=doctor,HLP=doctor.hospital.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,is_rejected = False).filter(applied_date__gte=showdate).order_by('applied_date')

            bookings_now = OrderBooking.objects.filter(hospitalstaffdoctor=doctor,HLP=doctor.hospital.admin,is_taken=False,is_otp_verified=False,is_active=True,is_cancelled = False,applied_date=showdate,is_rejected = False).order_by('applied_date')
        else:
            bookings = OrderBooking.objects.filter(HLP=doctor.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,is_rejected = False).order_by('applied_time')

            upcoming_bookings = OrderBooking.objects.filter(HLP=doctor.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,is_rejected = False).filter(applied_date__gte=showdate).order_by('applied_date')

            bookings_now = OrderBooking.objects.filter(HLP=doctor.admin,is_taken=False,is_otp_verified=False,is_cancelled = False,applied_date=showdate,is_rejected = False).order_by('applied_date')
            print(bookings)
            print(upcoming_bookings)
            print(bookings_now)
        

        param = {'bookings':bookings,'bookings_now':bookings_now,'upcoming_bookings':upcoming_bookings}
        return render(request,"doctor/newindex.html",param)        
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,e)
        #     return render(request,"doctor/newindex.html")
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

class doctorUpdateViews(SuccessMessageMixin,UpdateView):
    UserModel=get_user_model()
    def get(self, request, *args, **kwargs):
        hospital = None
        # contacts = None
        # insurances = None
        try:
            doctor = HospitalDoctors.objects.get(admin=request.user.id)      
            specailists = Specailist.objects.all()      
        except Exception as e:
            return None
        param={'hospital':doctor,'specailists':specailists}
        return render(request,"doctor/doctor-profile-settings.html",param) 
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get("fisrt_name")
        last_name = request.POST.get("last_name")
        name_title = request.POST.get("name_title")
        user_type = 3
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        profile_pic = request.FILES.get("profile_pic")
        # for HospitalDoctor user Creation
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        ssn_id = request.POST.get("ssn_id")
        country = request.POST.get("country")
        pin_code = request.POST.get("pin_code")
        dob = request.POST.get("dob")
        alternate_mobile = request.POST.get("alternate_mobile")
        gender = request.POST.get("gender")
        # for Hospital staff user creation
        joindate = request.POST.get("joindate")
        is_active = request.POST.get("is_active")
        opd_charges = request.POST.get("opd_charges")
        home_charges = request.POST.get("home_charges")
        is_homevisit_available = request.POST.get("is_homevisit_available")
        online_charges = request.POST.get("online_charges")
        emergency_charges = request.POST.get("emergency_charges")
        active = False
        if is_active == "Yes":
            active= True

        is_homevisi = request.POST.get("is_homevisit_available")
        is_homevisit_available = False
        if is_homevisi == "Yes":
            is_homevisit_available= True
    
        is_virtual = request.POST.get("is_virtual_available")
        is_virtual_available = False
        if is_virtual == "Yes":
            is_virtual_available = True
            
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        linkedin = request.POST.get("linkedin")
        degree = request.POST.get("degree")       
        specialist = request.POST.get("specialist")

        about = request.POST.get("about")          
        try:           
            hospital = HospitalDoctors.objects.get(admin=request.user.id)
            hospital.name_title=name_title
            hospital.fisrt_name=first_name
            hospital.last_name=last_name
            hospital.about=about
            hospital.address=address
            hospital.city=city
            hospital.pin_code=pin_code
            hospital.state=state
            hospital.country=country
            hospital.phone=phone
            if specialist:
                specialist1 = get_object_or_404(Specailist,id=specialist)
                hospital.specialist=specialist1

            if profile_pic:
                hospital.profile_pic=profile_pic
                hospital.admin.profile_pic=profile_pic    
                
            hospital.degree=degree
            hospital.alternate_mobile=alternate_mobile
            hospital.linkedin=linkedin
            hospital.facebook=facebook
            hospital.instagram=instagram
            hospital.dob=dob
            hospital.is_appiled=True
            hospital.is_active=active
            hospital.is_virtual_available=is_virtual_available
            hospital.is_homevisit_available=is_homevisit_available
            hospital.is_verified=False
            hospital.gender=gender
            hospital.opd_charges=opd_charges
            hospital.online_charges=online_charges
            hospital.emergency_charges=emergency_charges
            hospital.home_charges=home_charges
            hospital.is_hospital_added=False
            hospital.save()
            #edit customUSer
            hospital.admin.first_name=first_name
            hospital.admin.last_name=last_name
            hospital.admin.name_title=name_title       
            
            hospital.admin.save()
            
           
                
            
            print("All data saved")

           
            # except:
            #     return render(request,"radmin/hospital_add.html") 
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)

        messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
        return HttpResponseRedirect(reverse("hospital_update"))



"""
Patient creations just for hosiptal visit patients but for backend i and adding patient cardential
"""
class managePatientView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            doctor=HospitalDoctors.objects.get(admin=request.user)
            hos_patients = Patients.objects.filter(doctor=doctor,is_active=True)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_patient"))        
        param={'doctor':doctor,'hos_patients':hos_patients}
        return render(request,"doctor/manage_patient.html",param)        

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
        blood_docation_date = request.POST.get("blood_docation_date")
        bloodgroup = request.POST.get("bloodgroup")
       
        # for Hospital staff user creation

        if ID_proof:
            ID_proof_url = ID_proof

        p=CustomUser.objects.filter(phone=phone).count()
        e=CustomUser.objects.filter(email=email).count()
        if p > 0:
            msg=messages.error(request,"Phone Already Exits")
            return HttpResponseRedirect(reverse("doc_manage_patient"))        
        if e > 0:
            msg=messages.error(request,"Email Already Exits")
            return HttpResponseRedirect(reverse("doc_manage_patient"))        
       
        doctor=HospitalDoctors.objects.get(admin=request.user)

        
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
        account.patients.country = "India"
        account.patients.pin_code = pin_code
        account.patients.dob = dob
        account.patients.age = age
        account.patients.alternate_mobile = alternate_mobile
        account.patients.profile_pic = profile_pic
        account.patients.gender = gender
        account.patients.bloodgroup = bloodgroup
        account.patients.doctor = doctor
        account.patients.status = status
        account.patients.added_by_doctor = True 
        account.patients.is_active = True 
        account.patients.save()   
        account.save()
       
        messages.add_message(request,messages.SUCCESS,"Successfully Added")
        return HttpResponseRedirect(reverse("doc_manage_patient"))

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

        if ID_proof:
            ID_proof_url = ID_proof
           
        doctor=HospitalDoctors.objects.get(admin=request.user)     
        """
       Updating Hospital Patient for now
        """
        patient = get_object_or_404(Patients,id=id)

        patient.admin.name_title = name_title
        patient.admin.first_name = first_name
        patient.admin.last_name = last_name
        patient.fisrt_name = first_name
        patient.last_name = last_name
        patient.address = address
        patient.city = city
        patient.state = state
        patient.country = "India"
        patient.pin_code = pin_code
        patient.dob = dob
        patient.age = age
        patient.alternate_mobile = alternate_mobile
        patient.profile_pic = profile_pic
        patient.gender = gender
        patient.bloodgroup = bloodgroup
        patient.doctor = doctor
        patient.ID_number = ID_number
        patient.ID_proof = ID_proof_url
        patient.status = status 
        patient.added_by_doctor = True 
        patient.is_active = True 
        patient.save()   
        patient.admin.save()
       
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
        return HttpResponseRedirect(reverse("manage_patient"))

def deleteDoctorPatient(request,id):
    doctor=HospitalDoctors.objects.get(admin=request.user)  
    patient = Patients.objects.get(id=id,doctor=doctor)
    patient.is_active=False
    patient.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("doc_manage_patient"))

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

"""Reviews list and edit delete """
class DoctorReviewsListView(SuccessMessageMixin,ListView):
     def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.filter(HLP = request.user)
            total_review = RatingAndComments.objects.filter(HLP = request.user).count()
            print(review_list)
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"doctor/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("doctor_reviews")) 


"""
Update appointment yet not implemented will think more that
"""

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
        return render(request,"doctor/manage_treatment.html",param)        

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
            hospitaldoctors=HospitalDoctors.objects.get(admin=request.user)
            treatmentreliefpetient = TreatmentReliefPetient.objects.get(is_active=True,id=id)
            oldbooking = TreatmentReliefPetient.objects.filter(is_active=True,patient=treatmentreliefpetient.patient)
            # hospitaldoctors = HospitalDoctors.objects.filter(hospital=hospital,is_active=True)
            # serviceandcharges = ServiceAndCharges.objects.filter(user=hospital.admin)
            patientfiles = patientFile.objects.filter(treatmentreliefpetient=treatmentreliefpetient) 
            # slot = Slot.objects.filter(patient=treatmentreliefpetient.patient.admin) # yet not required
            # labtests =LabTest.objects.filter(slot__patient=treatmentreliefpetient.patient.admin,is_active=True,slot__send_to_doctor=True)
            # print(labtests)
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("doc_manage_relief_patient"))        
        param={'treatmentreliefpetient':treatmentreliefpetient,'oldbooking':oldbooking,'hospitaldoctors':hospitaldoctors,'patientfiles':patientfiles}
        return render(request,"doctor/patient_profile.html",param)        
 
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
            return HttpResponseRedirect(reverse("doc_relief_patient_profile",kwargs={'id':treatmentreliefpetient.id}))
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("relief_patient_profile",kwargs={'id':treatmentreliefpetient.id}))
    

class manageReliefPatientViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try:
            doctor=HospitalDoctors.objects.get(admin=request.user)
            treatmentreliefpetient = TreatmentReliefPetient.objects.filter(is_active=True,booking__is_taken=True,booking__hospitalstaffdoctor=doctor)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("doc_manage_relief_patient"))        
        param={'doctor':doctor,'treatmentreliefpetient':treatmentreliefpetient}
        return render(request,"doctor/manage_relief_patient.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
           
        try:
            pass
        except Exception as e:
            print(e)
            # return HttpResponse(e)
       
        print("Appoinment update saved")      
        return HttpResponseRedirect(reverse("doc_manage_relief_patient"))

def deleteReliefDoctorPatient(request,id):
    patient = TreatmentReliefPetient.objects.get(id=id)
    patient.is_active=False
    patient.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("manage_relief_patient"))

""""New Doctor schedule"""

""""NEW DOCTORS SLOT IN BOX"""
class DoctorScheduleCreateView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        doctor = request.user.hospitaldoctors
        dates = DoctorSchedule.objects.filter(doctor=doctor).values('scheduleDate','id')
        schedule_dates ={item['scheduleDate'] for item in dates}
        schedule_dates_list = []
        for sch_Dat in schedule_dates:
            scd_type = DoctorSchedule.objects.filter(scheduleDate=sch_Dat,doctor=doctor).first()
            scd_type_all = DoctorSchedule.objects.filter(scheduleDate=sch_Dat,doctor=doctor)
            schedule_dates_list.append({'scd_type':scd_type,'sch_Dat':sch_Dat,'scd_type_all':scd_type_all})
            
            # sch_type = DoctorSchedule.objects.values('scheduleDate','id')
        print(schedule_dates_list)


        # schedule_dates = DoctorSchedule.objects.filter()
        timeslots_15s = TimeSlot.objects.filter(schedule_type="15")
        timeslots_30s = TimeSlot.objects.filter(schedule_type="30")
        timeslots_45s = TimeSlot.objects.filter(schedule_type="45")
        timeslots_60s = TimeSlot.objects.filter(schedule_type="60")

        param = {'timeslots_15s':timeslots_15s,'timeslots_30s':timeslots_30s,'timeslots_45s':timeslots_45s,'timeslots_60s':timeslots_60s,'doctor':doctor,'schedule_dates_list':schedule_dates_list}
       
        return render(request,'doctor/view-doctor-schedule.html',param)
    
    def post(self, request, *args, **kwargs):
        timeslot_list = request.POST.getlist('timeslot[]')
        scheduleDate = request.POST.get('scheduleDate')
        days = request.POST.get('days')

        doctor = get_object_or_404(HospitalDoctors,admin=request.user)
        for x in range(int(days)):
            newdate = datetime.strptime(scheduleDate,"%Y-%m-%d") + timedelta(days=int(x))
            doctorschedules = DoctorSchedule.objects.filter(doctor = doctor)
            for doctorschedule in doctorschedules:
                print(doctorschedule.scheduleDate)
                print(newdate.date())
                if doctorschedule.scheduleDate == newdate.date():
                    messages.add_message(request,messages.ERROR,"Already Booked date please delete if you want to change")
                    return HttpResponseRedirect(reverse("doc_manage_doctorschedule"))
            is_active =True
            for timeslot in timeslot_list:
                timeslot_obj = get_object_or_404(TimeSlot,id=timeslot)
                doctorschedule = DoctorSchedule(scheduleDate=newdate,doctor=doctor,is_active=is_active,timeslot=timeslot_obj)
                doctorschedule.save()
        messages.add_message(request,messages.SUCCESS,"Suucessfully Created")
        return HttpResponseRedirect(reverse("doc_manage_doctorschedule"))
 
def deleteTimeSlot(request,id):
    doctor = request.user.hospitaldoctors
    date1 = DoctorSchedule.objects.get(doctor=doctor,id=id)
    dates = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date1.scheduleDate)
    for date in dates:
        date.delete()
    messages.add_message(request,messages.SUCCESS,"Sucessfully Deleted")
    return HttpResponseRedirect(reverse("doc_manage_doctorschedule"))

""" Blog """

class addBlogView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):        
        # hospital=Hospitals.objects.get(admin=request.user) 
        doctor = request.user.hospitaldoctors
        blogs = Blog.objects.filter(doctor=doctor)
        param={'blogs':blogs,'doctors':doctor}
        return render(request,"doctor/add-blog.html",param)  

    def post(self, request, *args, **kwargs):
        blog_title = request.POST.get('blog_title')         
        content = request.POST.get('content')
        blog_image = request.FILES.get('blog_image')
        doctor = request.user.hospitaldoctors
        try:        
            blog = Blog(blog_title=blog_title,blog_content=content,doctor=doctor)
            if blog_image:
                blog.blog_image=blog_image
            blog.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("add_blog"))
        return HttpResponseRedirect(reverse("list_blog"))
 
class EditBlogUpdateView(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        print("no error till here i am at editblogupdateview")
        id=kwargs['id']        
        blog =get_object_or_404(Blog,id=id)
        # hospital=Hospitals.objects.get() 
        doctor = HospitalDoctors.objects.get(admin=request.user)
        param={'blog':blog,'doctor':doctor}
        return render(request,"doctor/edit-blog.html",param)  
    
    def post(self, request, *args, **kwargs):
        id=kwargs['id']   
        blog_title = request.POST.get('blog_title')         
        content = request.POST.get('content')
        blog_image = request.FILES.get('blog_image')
        # doctor = request.POST.get('doctor')
        try:
            doctor = get_object_or_404(HospitalDoctors,admin=request.user)
            blog =get_object_or_404(Blog,id=id)
            blog.blog_title=blog_title
            blog.blog_content=content
            blog.doctor=doctor
            if blog_image:
                blog.blog_image=blog_image
            blog.save()
   
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
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
    template_name = "doctor/blog.html"

class ReviewsList(ListView):
    model = RatingAndComments 
    template_name = "doctor/reviews.html" 

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
        doctor = get_object_or_404(HospitalDoctors,admin=request.user)        
        hos_diseases = HospitalDisease.objects.filter(doctor=doctor)
        diseases = Disease.objects.filter(is_active=True)
        param={'diseases':diseases,'hos_diseases':hos_diseases}
        return render(request,"doctor/add-disease.html",param)  

    def post(self, request, *args, **kwargs):
        name_list = request.POST.getlist('name []') 
        try:
            doctor = get_object_or_404(HospitalDoctors,admin=request.user)
            hos_des_dl = HospitalDisease.objects.filter(doctor=doctor)
            for hos in hos_des_dl:
                hos.delete()      
            for name in name_list:
                ds = get_object_or_404(Disease,id=name)
                hospitaldiseas = HospitalDisease(doctor=doctor,disease = ds)
                hospitaldiseas.save()
            messages.add_message(request,messages.SUCCESS,"Successfully Added")
        except Exception as e:
            messages.add_message(request,messages.ERROR,"Something Wrong with connnections")
            return HttpResponseRedirect(reverse("doc_manage_disease"))
        return HttpResponseRedirect(reverse("doc_manage_disease"))


