from datetime import datetime, date, timedelta
from webbrowser import get
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.db.models import deletion
from django.db.models.base import Model
from django.db.models.query_utils import Q
from django.http.request import HttpRequest
from accounts.views import send_otp
from chat.models import Notification
from front.models import RatingAndComments
from lab.models import LabSchedule, Medias
from django.views.generic.base import View
# from requests.models import Response
from hospital.models import DoctorSchedule, HospitalMedias, HospitalStaffDoctorSchedual, ServiceAndCharges
from patient import models
import patient
from patient.models import Booking, ForSome, MediacalRecords, NewLabTest, OrderBooking, Orders, LabTest, PicturesForMedicine, Temp, Slot, patientFile, phoneOPTforoders
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from accounts.models import CustomUser, HospitalDoctors, HospitalPhones, Hospitals, Labs, OPDTime, Patients, Pharmacy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls.base import resolve, reverse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from accounts.utils import generate_token
import base64
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
import random
import http.client
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, message

conn = http.client.HTTPConnection("2factor.in")
from django.utils.decorators import method_decorator
from django.db.models.signals import post_save
from channels.layers import get_channel_layer 
from django.db import transaction
# Create your views here.  
class generateKey:
    @staticmethod
    def returnValue(bookindId):
        return str(bookindId) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

def verifyOTP(request,orderID):
    # try:
    #     order = get_object_or_404(Orders,id=orderID) #booking id find
    # except Exception as e:
    #     messages.add_message(request,messages.ERROR,"Booking id number does not Exits")
    #     return HttpResponseRedirect(reverse("hospitalsingup"))  # False Call
    # if request.POST:
    #     first=request.POST.get("first")
    #     second=request.POST.get("second")
    #     third=request.POST.get("third")
    #     forth=request.POST.get("forth")
    #     fifth=request.POST.get("fifth")
    #     sixth=request.POST.get("sixth")

    #     postotp = first+second+third+forth+fifth+sixth  #added in one string

    #     keygen = generateKey()
    #     key = base64.b32encode(keygen.returnValue(orderID).encode())  # Generating Key
    #     OTP = pyotp.HOTP(key)  # HOTP Model
    #     if OTP.verify(postotp, order.counter):  # Verifying the OTP
    #         order.is_booking_Verified = True
    #         order.taken_date_time=True
    #         order.save()
    #         messages.add_message(request,messages.SUCCESS,"Mobile Verified Successfuly")
    #     #emila message for email verification
    #     current_site=get_current_site(request) #fetch domain    
    #     email_subject='Active your Account',
    #     message=render_to_string('accounts/activate.html',
    #     {
    #         'user':user,
    #         'domain':current_site.domain,
    #         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #         'token':generate_token.make_token(user)
    #     } #convert Link into string/message
    #     )
    #     print(message)
    #     email_message=EmailMessage(
    #         email_subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [user.email]
    #     )#compose email
    #     print(email_message)
    #     email_message.send() #send Email
    #     messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")        
        return HttpResponseRedirect(reverse("dologin"))
        # return HttpResponseRedirect(reverse("dologin"))

"""
Personal Details of Patients
""" 
class patientdDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        try:
            booked = OrderBooking.objects.filter(patient = request.user,booking_for = "H")
            labbooks = OrderBooking.objects.filter(patient = request.user,booking_for = "L")
            booking_labtest_list =[]
            for labbook in labbooks:            
                labtests = NewLabTest.objects.filter(booking=labbook)
                booking_labtest_list.append({'labbook':labbook,'labtests':labtests})
            phamacybooking = OrderBooking.objects.filter(patient = request.user,booking_for = "P")
            print(booked)
            param = {'booked':booked,"booking_labtest_list":booking_labtest_list,'phamacybooking':phamacybooking}
            # if patient.fisrt_name and patient.last_name and patient.address and patient.city and patient.zip_Code and patient.state and patient.country and patient.dob and patient.profile_pic and patient.gender and patient.bloodgroup:
            
            return render(request,"patient/patient-dashboard.html",param)            
            # else:
            #     messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            
            # return render(request,"patient/patient_update.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    
class patientdUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        try: 
            patient = get_object_or_404(Patients, admin=request.user.id)
            return render(request,"patient/profile-settings.html",{'patient':patient})
        except Exception as e:
            return HttpResponse(e)
    
    def post(self,request, *agrs, **kwargs):
        profile_pic = request.FILES.get('profile_pic') 
        name_title = request.POST.get('name_title')
        fisrt_name = request.POST.get('fisrt_name')
        last_name = request.POST.get('last_name')
        alternate_mobile = request.POST.get('alternate_mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_Code = request.POST.get('zip_Code') 
        state = request.POST.get('state')
        country = request.POST.get('country')
        gender = request.POST.get('gender')
      
        dob = request.POST.get('dob')
        
        bloodgroup = request.POST.get('bloodgroup')
        blood_docation_date = request.POST.get('blood_docation_date')
        blood_donation = request.POST.get('blood_donation')
        print(blood_donation)
        print(gender)
        print(blood_docation_date)
        # if blood_donation:
        #     blood_donation = True
        # else:
        #     blood_donation = False

        age1 = (date.today() - datetime.strptime(dob, "%Y-%m-%d").date()) // timedelta(days=365.2425)
       
        # import datetime
        # age = (datetime.date.today() - datetime.datetime.strptime(dob, "%Y-%m-%d").date())/365
        # try: 
        print(name_title,profile_pic,alternate_mobile,address,city,state,zip_Code,country,gender,bloodgroup,age1)
        user= request.user
        print(user.first_name)         
        print(user.last_name)         
        # user.patients.name_title=name_title
        user.name_title=name_title
        user.first_name = fisrt_name
        user.last_name = last_name
        user.patients.fisrt_name=fisrt_name
        user.patients.last_name=last_name
        if profile_pic:
            fs=FileSystemStorage()
            filename1=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename1)
            user.patients.profile_pic=profile_pic_url
            user.profile_pic = profile_pic_url
        user.patients.alternate_mobile=alternate_mobile
        user.patients.address=address
        user.patients.city=city
        user.patients.state=state
        user.patients.zip_Code=zip_Code
        user.patients.country=country
        user.patients.gender=gender
        user.patients.dob=dob 
        user.patients.bloodgroup=bloodgroup
        user.patients.age=age1
        user.patients.blood_docation_date=blood_docation_date
        user.patients.blood_donation=blood_donation
        user.patients.is_verified = True         
        user.patients.save()
        user.save()
        messages.add_message(request,messages.SUCCESS,"User Detail updates Successfully !")
        return HttpResponseRedirect(reverse("patient_home"))
        # except Exception as e:
        #     return HttpResponse(e)
"""Medical files"""

class RecordsViews(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        files = MediacalRecords.objects.filter(patient__admin = request.user,is_active=True)
        relief_files = patientFile.objects.filter(patient__admin = request.user)
        someones = ForSome.objects.filter(patient__admin = request.user)
        hospitals = Hospitals.objects.filter(admin__is_active=True,is_verified=True,is_deactive=False)
        return render(request,"patient/medical-records.html",{"files":files,'relief_files':relief_files,'someones':someones,'hospitals':hospitals})    
        
    def post(self,request, *agrs, **kwargs):
        for_whom = request.POST.get('someone')
        hospital = request.POST.get('hospital') 
        prescription = request.FILES.get('prescription')
        symptoms = request.POST.get('symptoms')
        AppoinmentDate = request.POST.get('AppoinmentDate')
        print(for_whom,hospital,prescription,symptoms,AppoinmentDate)
        hospital1 = Hospitals.objects.get(id=hospital)        
        # try:
        addmedical = MediacalRecords(symptoms=symptoms,is_active=True,AppoinmentDate=AppoinmentDate,hospital=hospital1,patient = request.user.patients)
        print()
        if for_whom:
            for_whom1 = ForSome.objects.get(id=for_whom)
            addmedical.for_whom=for_whom1
        if prescription:
            fs=FileSystemStorage()
            filename1=fs.save(prescription.name,prescription)
            prescription_url=fs.url(filename1)
            addmedical.prescription=prescription_url
        addmedical.save()
        print(addmedical)
        messages.add_message(request,messages.SUCCESS,"Madical Record Created successfully !")
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,e)
        return HttpResponseRedirect(reverse("records"))

def DeleteMedicalFiles(request,id):
    addmedical = get_object_or_404(MediacalRecords,id=id)
    addmedical.is_active=False
    addmedical.save()
    messages.add_message(request,messages.SUCCESS,"Madical Record Deleted successfully !")
    return HttpResponseRedirect(reverse("records"))

"""" 
Hospital list and profile
"""
class HospitalListViews(ListView):
    # context_object_name = "hospital"
    paginate_by = 10
    model = Hospitals
    template_name = "patient/hospital_list.html"
    # paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            hospitals=Hospitals.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            hospitals=Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        hospital_media_list = []
        for hospital in hospitals:
            medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)           
            hospital_media_list.append({'hospital':hospital,'medias':medias})
        print(hospital_media_list)        
        return hospital_media_list
   
    def get_context_data(self,**kwargs):
        context=super(HospitalListViews,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

    # def get(self, request, *args, **kwargs):        
    #     hospitals = Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
    #     hospital_media_list = []
    #     for hospital in hospitals:
    #         medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)           
    #         hospital_media_list.append({'hospital':hospital,'medias':medias})
    #     param = {'hospital_media_list':hospital_media_list}  
    #     return render(request,"patient/hospital_list.html",param)


""""  
History for Hospital Booking
"""
class ViewBookedAnAppointmentViews(SuccessMessageMixin,ListView):
   
    def get(self,request):
        booked = OrderBooking.objects.filter(patient = request.user,booking_for = "H")
        labbooks = OrderBooking.objects.filter(patient = request.user,booking_for = "L")
        booking_labtest_list =[]
        for labbook in labbooks:            
            labtests = LabTest.objects.filter(slot=labbook)
            booking_labtest_list.append({'labbook':labbook,'labtests':labtests})
        phamacybooking = OrderBooking.objects.filter(patient = request.user,booking_for = "P")
        print(booked) 
       
        param = {'booked':booked,"booking_labtest_list":booking_labtest_list,'phamacybooking':phamacybooking}
         
        return render(request,"patient/patient-dashboard.html",param)

def bookingConfirmation(request,booking_id):
    try:
        booking = get_object_or_404(Booking,id=booking_id,patient=request.user )
        notifications = Notification.objects.filter(booking=booking,to_user=request.user)
        for notification in notifications:
            notification.user_has_seen =True
            notification.save()
        context = {'booking' : booking}
        return render(request , 'patient/confirmation.html', context)
    except Exception as e:
        messages.add_message(request,messages.ERROR,"page not found!")
        return render(request , 'accounts/404.html',)

class BookAnAppointmentViews(SuccessMessageMixin,View):
    def post(self,request, *args, **kwargs):
        # try:
        doctorid = request.POST.get('doctor_id')       
        timeslot = request.POST.get('timeslot')
        serviceid_list = request.POST.getlist('serviceid[]')
        someone = request.POST.get('someone')       
        date = request.POST.get('date')       
        where = request.POST.get('orderwhere')
        booking_type = request.POST.get('booking_type')
        now = datetime.now()
        now5 = now + timedelta(minutes=5)
        
        with transaction.atomic():
            booking = OrderBooking(patient = request.user,applied_date=date,is_applied=True,is_active=True,status="BOOKED")
            booking.reject_within_5__lt = now            
        booking.reject_within_5 = now5
        booking.payment_status="INPROCESS"
        if someone:
            forsome = get_object_or_404(ForSome,id=someone)
            booking.for_whom=forsome
        if where == "hospital":
            hospitalstaffdoctor = get_object_or_404(HospitalDoctors,id=doctorid)
            doctorschedule = get_object_or_404(DoctorSchedule,id=timeslot,doctor=hospitalstaffdoctor)
            doctorschedule.is_booked =True
            doctorschedule.save()
            booking.applied_time=doctorschedule.timeslot.schedule
            booking.hospitalstaffdoctor=hospitalstaffdoctor
            booking.HLP=hospitalstaffdoctor.hospital.admin
            booking.booking_for="H"
            booking.booking_type=booking_type           
            if booking_type == "EMERGENCY": 
                booking.amount=hospitalstaffdoctor.emergency_charges
            if booking_type == "OPD":
                booking.amount=hospitalstaffdoctor.opd_charges
            if booking_type == "ONLINE":
                booking.amount=hospitalstaffdoctor.online_charges
            if booking_type == "HOMEVISIT":
                booking.amount=hospitalstaffdoctor.home_charges
            someones = ForSome.objects.filter(patient=request.user.patients )
            param = {'booking':booking,'someones':someones}
        if where == "lab": 
            booking.booking_for="L"
            lab = get_object_or_404(Labs,id=doctorid)
            labschedule = get_object_or_404(LabSchedule,id=timeslot,lab=lab)
            labschedule.is_booked =True
            labschedule.save()
            booking.applied_time=labschedule.timeslot.schedule
            booking.HLP=lab.admin
            booking.booking_type=booking_type
            total = 0
            booking.save()
            for service in serviceid_list:
                ser = get_object_or_404(ServiceAndCharges,id=service)
                labtest = NewLabTest(booking=booking,service=ser)
                labtest.save()       
                total = total + ser.service_charge
            booking.amount = total
            someones = ForSome.objects.filter(patient=request.user.patients )
            param = {'booking':booking,'someones':someones}
        booking.save()
        tc = 0
        try:
            tc = Temp.objects.filter(user=request.user).count()
        except:
            tc = 0
        print("tc check below")
        print(tc)
        if tc > 0:
            temp = Temp.objects.get(user=request.user)
            temp.delete()
        temp =  Temp(user=request.user,order_id=booking.order_id)
        temp.save() 
        
        print(booking.reject_within_5__lt)
        print(booking.reject_within_5)
 
        print("booking saved")
        mobile= request.user.phone
        key = send_otp(mobile)
        print(key)
        if key: 
            obj = phoneOPTforoders(order_id=booking,user=request.user,otp=key)
            obj.save()
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.HLP,booking=booking)
            notification.save()
                # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                # res = conn.getresponse()
                # data = res.read()
                # data=data.decode("utf-8")
                # data=ast.literal_eval(data)
                # print(data)            
            return JsonResponse({'message' : 'success','status': True,'Booking_id':booking.id,"otp":key})
        else:
            return JsonResponse({'message' : 'Error','status': False})

    def new_method(self, now, booking):
        booking.reject_within_5__lt = now
    
   
    # except Exception as e:
    #         messages.add_message(request,messages.ERROR,"Network Issue try after some time")
    #         return HttpResponse(e)

            
            # import checksum generation utility
            # You can get this utility from https://developer.paytm.com/docs/checksum/
          
            # paytmParams = dict()

            # paytmParams["body"] = {
            #     "requestType"   : "Payment",
            #     "mid"           : "Vsrdcl31860853647501",
            #     "websiteName"   : "WEBSTAGING",
            #     "orderId"       : str(booking.id),
            #     "callbackUrl"   : "http://127.0.0.1:8000/patient/handlerequest",
            #     "txnAmount"     : {
            #         "value"     : str(booking.amount),
            #         "currency"  : "INR",
            #     },
            #     "userInfo"      : {
            #         "custId"    : str(request.user.phone),
            #     },
            # }

            # # Generate checksum by parameters we have in body
            # # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
            # checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "JDhgGD%hhT&OtVEE")

            # paytmParams["head"] = {
            #     "signature"    : checksum
            # }
            

            # post_data = json.dumps(paytmParams)

            # # for Staging
            # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=Vsrdcl31860853647501&orderId="+str(booking.id)

            # # for Production
            # # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            # response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
            # print(response)
            # print(response['body']['txnToken'])
            
           
            # paytmParams["head"] = {
            #     "tokenType"     : "TXN_TOKEN",
            #     "token"         : response['body']['txnToken']
            # }
            # post_data = json.dumps(paytmParams)

            # # for Staging
            # url = "https://securegw-stage.paytm.in/theia/api/v2/fetchPaymentOptions?mid=Vsrdcl31860853647501&orderId="+str(booking.id)
            

            # # for Production
            # # url = "https://securegw.paytm.in/theia/api/v2/fetchPaymentOptions?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            # response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
            # print(response)        

def CancelBookedAnAppointmentViews(request,id):
    booked = Booking.objects.get(id=id)
    booked.is_cancelled = True
    booked.Status = "cancelled"
    booked.save()
    messages.add_message(request,messages.SUCCESS,"Cancelled Successfully !")
    return HttpResponseRedirect(reverse('viewbookedanappointment'))

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        print(key)
        return key
    else:
        return False

""""
History for Lab Booking
"""

class BookAnAppointmentForLABViews(SuccessMessageMixin,View):
    def post(self,request, *args, **kwargs):        
        if request.method == "POST":
            serviceid_list = request.POST.getlist('serviceid[]')
            date = request.POST.get('date')
            labid = request.POST.get('labid')
            someone = request.POST.get('someone')
            lab = get_object_or_404(Labs,id=labid)
            time = request.POST.get('time') 
            print(serviceid_list,date,labid,lab,time)
            if someone:
                forsome = get_object_or_404(ForSome,id=someone)
                labbooking = Slot(patient = request.user,for_whom=forsome,lab=lab,applied_date=date,applied_time=time,is_applied=True,is_active=True,status="booked") 
            else:   
                labbooking = Slot(patient = request.user,lab=lab,applied_date=date,applied_time=time,is_applied=True,is_active=True,status="booked") 
            labbooking.save()
            total = 0
                        
            for serviceid in serviceid_list:
                service = ServiceAndCharges.objects.get(id=serviceid)
                labservices = LabTest(service=service,lab=lab,slot=labbooking,is_active=True)
                labservices.save()
                total =total + service.service_charge 
            labbooking.amount=total
            labbooking.save()
            print("booking saved")
            order = Orders(patient=request.user,service=service,booking_for=2,bookingandlabtest=labbooking.id,amount=total,status=1)
            order.save()
            print("order")
            tc = 0
            try:
                tc = Temp.objects.filter(user=request.user).count()
            except:
                tc = 0
            print("tc check below")
            print(tc)
            if tc > 0:
                temp = Temp.objects.get(user=request.user)
                temp.delete()
            temp =  Temp(user=request.user,order_id=order.id)
            temp.save() 
            print("temp")
            mobile= request.user.phone
            key = send_otp(mobile)
            print(key)
            if key:
                obj = phoneOPTforoders(order_id=order,user=request.user,otp=key)
                obj.save()
                notification =  Notification(notification_type="1",from_user= request.user,to_user=lab.admin,slot=labbooking)
                notification.save()
                # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                # res = conn.getresponse()
                # data = res.read()
                # data=data.decode("utf-8")
                # data=ast.literal_eval(data)
                # print(data)            
                return JsonResponse({'message' : 'success','status': True,'Booking_id':labbooking.id,"otp":key})
            else:
                return JsonResponse({'message' : 'error','status': False,})
           
        # except Exception as e:
        #     messages.add_message(request,messages.ERROR,"Network Issue try after some time")
        #     return HttpResponse(e)

def ReportSendToDoctorViews(request,id):
    slot = get_object_or_404(Slot,id=id)
    slot.send_to_doctor =True
    slot.save()
    messages.add_message(request,messages.SUCCESS,"Send to doctor Successfully !")
    return HttpResponseRedirect(reverse("viewbookedanappointment"))


def CancelLabBookedAnAppointmentViews(request,id):
    booked = Slot.objects.get(id=id)
    booked.is_cancelled = True
    booked.status = "cancelled"
    booked.save()
    messages.add_message(request,messages.SUCCESS,"Cancelled Successfully !")
    return HttpResponseRedirect(reverse('viewbookedanappointment'))
       
"""
Lab View and Profile 
"""
class LabListViews(ListView):
    def get(self, request, *args, **kwargs):
        labs = Labs.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
        lab_media_list = []
        for lab in labs:
            medias = Medias.objects.filter(is_active=True,user=lab.admin)           
            lab_media_list.append({'lab':lab,'medias':medias})
        print(lab_media_list)
        param = {'lab_media_list':lab_media_list}  
        return render(request,"patient/lab_list.html",param)
    
class labDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        lab = get_object_or_404(Labs,is_verified=True,is_deactive=False,id=lab_id)
        services = ServiceAndCharges.objects.filter(user=lab.admin)
        someones = ForSome.objects.filter(patient=request.user.patients)
        opdtime = OPDTime.objects.get(user=lab.admin)            
        param = {'lab':lab,'services':services,'opdtime':opdtime,'someones':someones}  
        return render(request,"patient/lab_details.html",param)


def slotConfirmation(request,slot_id):
    try:
        slot = get_object_or_404(Slot,id=slot_id,patient=request.user )
        notifications = Notification.objects.filter(slot=slot,to_user=request.user)
        for notification in notifications:
            notification.user_has_seen =True
            notification.save()
        context = {'slot' : slot}
        return render(request , 'patient/slotconfirmation.html', context)
    except Exception as e:
        messages.add_message(request,messages.ERROR,"page not found!")
        return render(request , 'accounts/404.html',)

"""
Pharmacy view and profile
"""

class PharmacyListViews(ListView):
    def get(self, request, *args, **kwargs):
        pharamcy = Pharmacy.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True)
        param = {'pharamcys':pharamcy} 
        print(pharamcy)
        return render(request,"patient/pharmacy_list.html",param)

class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        pharmacy_id=kwargs['id']
        pharmacy = get_object_or_404(Pharmacy,id=pharmacy_id)
        param = {'pharmacy':pharmacy} 
        return render(request,"patient/pharmacy_details.html",param)

class UploadPresPhotoViews(SuccessMessageMixin,View):
    def post(self,request, *args, **kwargs):
        
        if request.method == "POST": 
            prescription = request.FILES.get('prescription')
            if prescription:
                fs=FileSystemStorage()
                filename1=fs.save(prescription.name,prescription)
                profile_pic_url=fs.url(filename1)
            print(prescription)
            date = request.POST.get('date')
            pharmacyid = request.POST.get('pharmacyid')
            add_note = request.POST.get('add_note')
            pharmacy = get_object_or_404(Pharmacy,id=pharmacyid)
            time = request.POST.get('time') 
            print(time,date,pharmacy,pharmacyid,prescription)
            picturesformedicine = PicturesForMedicine(patient = request.user,pharmacy=pharmacy,prescription=profile_pic_url,applied_date=date,applied_time=time,is_applied=True,is_active=True,add_note=add_note,status="booked") 
            picturesformedicine.save()
            service = get_object_or_404(ServiceAndCharges,id=13)
            print("booking saved")
            order = Orders(patient=request.user,service=service,booking_for=3,bookingandlabtest=picturesformedicine.id,status=1,)
            order.save()
            print("order")
            tc = 0
            try:
                tc = Temp.objects.filter(user=request.user).count()
            except:
                tc = 0
            print("tc check below")
            print(tc)
            if tc > 0:
                temp = Temp.objects.get(user=request.user)
                temp.delete()
            temp =  Temp(user=request.user,order_id=order.id)
            temp.save() 
            print("temp")
            mobile= request.user.phone
            key = send_otp(mobile)
            print(key)
            if key:
                obj = phoneOPTforoders(order_id=order,user=request.user,otp=key)
                obj.save()
                notification =  Notification(notification_type="1",from_user= request.user,to_user=pharmacy.admin,picturesmedicine=picturesformedicine)
                notification.save()
                # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                # res = conn.getresponse()
                # data = res.read()
                # data=data.decode("utf-8")
                # data=ast.literal_eval(data)
                # print(data)
                return JsonResponse({'message' : 'success','status': True,'Booking_id':picturesformedicine.id,"otp":key})
            else:
                return JsonResponse({'message' : 'error','status': False,})
            # return render(request,"patient/amount_confirmation.html")
            # return HttpResponseRedirect(reverse("pharmacy_details" , kwargs={'id':pharmacyid}))

def picturesformedicineConfirmation(request,booking_id):   
    # try:
    picturesformedicine = get_object_or_404(PicturesForMedicine,id=booking_id,patient=request.user )
    notifications = Notification.objects.filter(picturesmedicine=picturesformedicine,to_user=request.user)
    for notification in notifications:
        notification.user_has_seen =True
        notification.save()
    print("hello i m in view of confirmation")
    context = {'picturesformedicine' : picturesformedicine}
    return render(request , 'patient/pharmacy_confirmation.html', context)
    # except Exception as e:
    #     messages.add_message(request,messages.ERROR,"page not found!")
    #     return render(request , 'accounts/404.html',)

def CancelPictureForMedicineViews(request,id):
    booked = PicturesForMedicine.objects.get(id=id)
    booked.is_cancelled = True
    booked.Status = "cancelled"
    booked.save()
    messages.add_message(request,messages.SUCCESS,"Cancelled Successfully !")
    return HttpResponseRedirect(reverse('viewbookedanappointment'))

"""
Add Someone As patient and Update  and delete

""" 
def helllo(request):
    return HttpRequest("hello")

class AddSomeoneAsPatient(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        patient=get_object_or_404(Patients,admin=request.user)
        someone = ForSome.objects.filter(patient=patient)
        param = {'someones':someone}
        return render(request,'patient/dependent.html',param)

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            where =request.POST.get("where")
            fisrt_name = request.POST.get("fisrt_name")
            last_name = request.POST.get("last_name")
            name_title = request.POST.get("name_title")
            age = request.POST.get("age")
            email = request.POST.get("email")
            add_notes = request.POST.get("add_notes")
            phone = request.POST.get("phone")
            ID_number = request.POST.get("ID_number")
            status = request.POST.get("status")
            ID_proof = request.FILES.get("ID_proof")
            profile_pic = request.FILES.get("profile_pic")
            address = request.POST.get("address")
            city = request.POST.get("city")
            gender = request.POST.get("gender")
            bloodgroup = request.POST.get("bloodgroup")
            id = request.POST.get("id")
            did = request.POST.get("did")
            someoneid = request.POST.get("someoneid")
            state = "Gujarat"
            country = "India"
            zip_Code = request.POST.get("zip_Code")
            relationship = request.POST.get("relationship")
            page_name = request.POST.get("page_name")
            print("inside add someone view")
            if where == "add":            
                # for Hospital staff user creation
                try:
                    profile_pic_url = ""
                   

                    ID_proof_url = ""
                    
                    print("insdie id_proof")     
                
                    patient=get_object_or_404(Patients,admin=request.user)
                    someone = ForSome(patient=patient,name_title=name_title,fisrt_name=fisrt_name,last_name=last_name,address=address,city=city,state=state,country=country,zip_Code=zip_Code,age=age,phone=phone,add_notes=add_notes,gender=gender,is_active=True,email=email,bloodgroup=bloodgroup,relationship=relationship)
                    if profile_pic:
                        fs=FileSystemStorage()
                        filename=fs.save(profile_pic.name,profile_pic)
                        media_url=fs.url(filename)
                        someone.profile_pic = media_url
                    if ID_proof:
                        fs1=FileSystemStorage()
                        filename=fs1.save(ID_proof.name,ID_proof)
                        id_media_url=fs1.url(filename)
                        someone.ID_proof = id_media_url   
                    someone.save()            
                    messages.add_message(request,messages.SUCCESS,"Successfully Added")
                    if page_name == "BOOKING":
                        return HttpResponseRedirect(reverse("bookappoinment", kwargs={'id':id,"did":did}))
                    if page_name == "HOMEVISIT":
                        return HttpResponseRedirect(reverse("home_visit_doctor", kwargs={'id':id,"did":did}))
                    if page_name == "OPD":
                        return HttpResponseRedirect(reverse("bookappoinment", kwargs={'id':id,"did":did}))
                    if page_name == "LAB":
                        return HttpResponseRedirect(reverse("laboratory_details", kwargs={'id':id}))
                    if page_name == "depedent_page":
                        return HttpResponseRedirect(reverse("add_someone_as_patient"))
                    # if page_name == "ONLINE":
                    # if page_name == "SETTING":
                except Exception as e:
                    return HttpResponse(e)
            elif where == "update":
                try:
                   
                    print("insdie id_proof")     
                
                    patient=get_object_or_404(Patients,admin=request.user)
                    someone = get_object_or_404(ForSome,id=someoneid)
                    someone.patient=patient
                    someone.name_title=name_title
                    someone.fisrt_name=fisrt_name
                    someone.last_name=last_name
                    someone.address=address
                    someone.city=city
                    someone.state=state
                    someone.country=country
                    someone.zip_Code=zip_Code
                    someone.age=age
                    someone.phone=phone
                    if ID_proof:
                        fs1=FileSystemStorage()
                        filename=fs1.save(ID_proof.name,ID_proof)
                        id_media_url=fs1.url(filename)
                        someone.ID_proof = id_media_url
                    someone.add_notes=add_notes
                    someone.gender=gender
                    someone.is_active=True
                    someone.email=email
                    someone.bloodgroup=bloodgroup
                    if profile_pic:
                        fs=FileSystemStorage()
                        filename=fs.save(profile_pic.name,profile_pic)
                        media_url=fs.url(filename)
                        someone.profile_pic= media_url
                    someone.relationship=relationship
                    someone.save()            
                    messages.add_message(request,messages.SUCCESS,"Successfully updated")
                    if page_name == "HOMEVISIT":
                        return HttpResponseRedirect(reverse("home_visit_doctor", kwargs={'id':id,"did":did}))
                    if page_name == "OPD":
                        return HttpResponseRedirect(reverse("bookappoinment", kwargs={'id':id,"did":did}))
                    if page_name == "LAB":
                        return HttpResponseRedirect(reverse("laboratory_details", kwargs={'id':id}))
                    if page_name == "depedent_page":
                        return HttpResponseRedirect(reverse("add_someone_as_patient"))
                except Exception as e:
                    return HttpResponse(e)       
            else:
                return HttpResponse("on other side")

def ForSomeDeactive(request,id):
    forsome =get_object_or_404(ForSome ,id=id)
    forsome.is_active =False
    forsome.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Deactivated")
    return HttpResponseRedirect(reverse("add_someone_as_patient"))

def ForSomeActive(request,id):
    forsome =get_object_or_404(ForSome ,id=id)
    forsome.is_active =True
    forsome.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Acticated")
    return HttpResponseRedirect(reverse("add_someone_as_patient"))

"""
Checkout page  
"""
def CheckoutViews(request):
    temp= Temp.objects.get(user=request.user)
    order = get_object_or_404(OrderBooking,order_id=temp.order_id)   
    book_for=order.booking_for
    if book_for == "H":
        param ={'booking':order}
    if book_for == "L":
        services = NewLabTest.objects.filter(booking=order)
        param ={'booking':order,'services':services}
    if book_for == "P":
        order.is_amount_paid = True
        order.store_invoice_uploaded = False
        order.status = "PAID"
        order.payment_status = "SUCCESS"
        order.save()
        param ={'booking':order}
    return render(request,"patient/checkout.html",param)



def PayForMedicine(request,id):
    booking = get_object_or_404(PicturesForMedicine,id=id)
    booking.amount_paid = True
    booking.status = "Amount Paid"
    booking.save()
    notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.pharmacy.admin,picturesmedicine=booking)
    notification.save()
    order = get_object_or_404(Orders,bookingandlabtest=booking.id,booking_for="3")
    order.status=1
    order.save()
    param ={'order':order,'booking':booking}
    return render(request,"patient/checkout.html",param)

def PaytmProcessViews(request):
    return HttpResponse("onpayment page")

"""
Paytm handler
"""
@csrf_exempt
def handlerequest(request):
    #paytm will send you post request here
    print("paytm came")
    # paytmParams = dict()
    # paytmChecksum = "CHECKSUM_VALUE"
    # paytmParams = request.form.to_dict()
    # paytmChecksum = paytmChecksum
    # paytmChecksum = paytmParams['CHECKSUMHASH']
    # paytmParams.pop('CHECKSUMHASH', None)

    # # Verify checksum
    # # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    # isVerifySignature = PaytmChecksum.verifySignature(paytmParams, "JDhgGD%hhT&OtVEE", paytmChecksum)
    # if isVerifySignature:
    #     print("Checksum Matched")
    # else:
    #     print("Checksum Mismatched")
    pass

"""
List of doctor or hospital for online
"""
def ListofVirtualDoctor(reuqest):
    return render(reuqest,"patient/virtual.html")

"""
Home visit doctor list
"""
class HomeVisitDoctor(CreateView):
    def get(self, request, *args, **kwargs):
        hospital_id= kwargs['id']
        hositaldcotorid_id= kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hospital_id)
        hospitalstaffdoctor = get_object_or_404(HospitalDoctors,is_active=True,id=hositaldcotorid_id)
        someones = ForSome.objects.filter(patient=request.user.patients)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
        param = {'someones':someones,'hospital':hospital,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalservice':hospitalservice}
        return render(request,"patient/home_visit.html",param)

def BookanAppointmentForHomeVisit(request):
   if request.method == "POST":
       if request.method == "POST":
            doctorid = request.POST.get('doctorid') 
            hospitalstaffdoctor = get_object_or_404(HospitalDoctors,id=doctorid)
            serviceid = request.POST.get('serviceid')
            someone = request.POST.get('someone')
            
            service = ServiceAndCharges.objects.get(id=serviceid)
            date = request.POST.get('date')
            time = request.POST.get('time')

            print(doctorid,hospitalstaffdoctor,serviceid,service,date,time)
            if someone:
                forsome = get_object_or_404(ForSome,id=someone)
                booking = Booking(patient = request.user,for_whom=forsome,hospitalstaffdoctor=hospitalstaffdoctor,service=service,applied_date=date,applied_time=time,is_applied=True,is_active=True,amount=service.service_charge,booking_type="HOME",status="booked")
            else:
                booking = Booking(patient = request.user,hospitalstaffdoctor=hospitalstaffdoctor,service=service,applied_date=date,applied_time=time,is_applied=True,is_active=True,amount=service.service_charge,booking_type="HOME",status="booked")
            booking.save()
            print("booking saved")
            order = Orders(patient=request.user,service=service,amount=service.service_charge,booking_for=1,bookingandlabtest=booking.id,status=1)
            order.save()
            print("order saved")
            if Temp.objects.get(user=request.user):
                temp = Temp.objects.get(user=request.user)
                temp.delete()
            temp =  Temp(user=request.user,order_id=order.id)
            temp.save()
            mobile= request.user.phone
            key = send_otp(mobile)
            print(key)
            if key:
                obj = phoneOPTforoders(order_id=order,user=request.user,otp=key)
                obj.save()
                # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
                # res = conn.getresponse()
                # data = res.read()
                # data=data.decode("utf-8")
                # data=ast.literal_eval(data)
                # print(data)            
                return JsonResponse({'message' : 'success','status': True,'Booking_id':booking.id,"otp":key})
            else:
                return JsonResponse({'message' : 'error','status': False,})


"""Reviews list and edit delete """
class PatineReviewsListView(SuccessMessageMixin,ListView):
     def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.filter(patient = request.user)
            total_review = RatingAndComments.objects.filter(patient = request.user).count()
            print(review_list)
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"patient/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("patine_reviews")) 
    
     def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("patine_reviews"))

