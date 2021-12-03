import json
from django.contrib.messages import views
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls.base import reverse
from django.views.generic import View,ListView,DetailView

from django.contrib import messages
from django.db.models import Q
from accounts.models import AdminHOD, Hospitals, Labs, Pharmacy, Specailist
from hospital.models import Blog, DoctorSchedule, HospitalMedias, HospitalStaffDoctors, ServiceAndCharges
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime,timedelta
# Create your views here.
  
class FrontView(View):
    def get(self, request, *args, **kwargs):
        
        hospitals=Hospitals.objects.filter(admin__is_active=True,is_verified = True,is_deactive=False)
        labs=Labs.objects.filter(admin__is_active=True,is_verified = True)
        pharmacys=Pharmacy.objects.filter(admin__is_active=True,is_verified = True)
        specilist = Specailist.objects.all()
        blogs = Blog.objects.filter(is_active=True)
        # departments = Departments.objects.filter(hospital=hospital)
        print(hospitals) 
        param={'hospitals':hospitals,'labs':labs,'pharmacys':pharmacys,'specilist':specilist,'blogs':blogs}
        return render(request,"front/index.html",param)

class BlogListView(ListView):
    model = Blog
    template_name = "front/blog-grid.html"
    paginate_by = 5
    queryset = Blog.objects.filter(is_active=True)

class BlogDetailsView(DetailView):
    model = Blog
    template_name = "front/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog_list"] = Blog.objects.filter(is_active = True) 
        return context
    
class SearchHospitalView(ListView):
    model = Hospitals
    template_name = "front/hospital-search.html"

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            hospitals=Hospitals.objects.filter( Q(is_verified=True,is_deactive=False,admin__is_active=True) and (Q(hopital_name__contains=filter_val) | Q(about__contains=filter_val) | Q(city__contains=filter_val) | Q(specialist__contains=filter_val))).order_by(order_by)
        else:
            hospitals=Hospitals.objects.filter(is_verified=True,is_deactive=False,admin__is_active=True).order_by(order_by)
        
        hospital_media_list = []
        for hospital in hospitals:
            print(hospital.admin)
            amount = ServiceAndCharges.objects.filter(user=hospital.admin,service_name = "OPD")
            print(amount)
            medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)           
            hospital_media_list.append({'hospital':hospital,'medias':medias,'amount':amount})
        print(hospital_media_list)        
        return hospital_media_list
    
    def get_context_data(self,**kwargs):
        context=super(SearchHospitalView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Hospitals._meta.get_fields()
        return context

class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id'] 
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        medias = HospitalMedias.objects.filter(is_active=True,hospital=hospital)  
        doctors = HospitalStaffDoctors.objects.filter(is_active=True,hospital=hospital)
        param = {'hospital':hospital,'medias':medias,'doctors':doctors}  
        return render(request,"front/new_hospital_details.html",param)

class DoctorsBookAppoinmentViews(View):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=hositaldcotorid_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,hospital=hospital)      
        token =False
        param = {'hospital':hospital,'doctor':doctor,'doctorschedules':doctorschedules,'token':token}  
        return render(request,"front/booking.html",param)
    
    def post(self, request, *args, **kwargs):
        doc_id = request.POST.get('doc_id')        
        date = request.POST.get('scheduleDate')
        if doc_id is None or date is None:
            doc_id=kwargs['did'] 
        doctor = get_object_or_404(HospitalStaffDoctors,is_active=True,id=doc_id)
        doctorschedules = DoctorSchedule.objects.filter(doctor=doctor,scheduleDate=date)
        print(date,doctor,doctorschedules)
        token = True
        param = {'hospital': doctor.hospital,'doctor':doctor,'doctorschedules':doctorschedules,'date':date,'token':token}  
        return render(request,"front/booking.html",param)



def CheckoutViews(request):
    if request.method == "POST":
        doctorid = request.POST.get('doctor_id')
        hospitalstaffdoctor = get_object_or_404(HospitalStaffDoctors,id=doctorid)
        timeslot = request.POST.get('timeslot')
        someone = request.POST.get('someone')       
        date = request.POST.get('date')
        doctorschedule = get_object_or_404(DoctorSchedule,id=timeslot,doctor=hospitalstaffdoctor)
        where = request.POST.get('where')
        booking_type = request.POST.get('booking_type')
        now = datetime.now()
        now5 = now + timedelta(minutes=5)
        
        with transaction.atomic():
            booking = OrderBooking(patient = request.user,applied_date=date,applied_time=doctorschedule.timeslot.schedule,is_applied=True,is_active=True,status="BOOKED")
            booking.reject_within_5__lt = now            
        booking.reject_within_5 = now5
        if someone:
            forsome = get_object_or_404(ForSome,id=someone)
            booking.for_whom=forsome
        if where == "hospital":
            booking.hospitalstaffdoctor=hospitalstaffdoctor
            booking.HLP=hospitalstaffdoctor.hospital.admin
            booking.payment_status="INPROCESS"
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
        booking.save()
        doctorschedule.is_booked =True
        doctorschedule.save()
        print(booking.reject_within_5__lt)
        print(booking.reject_within_5)
 
        print("booking saved")
        # tc = 0
        # try:
        #     tc = Temp.objects.filter(user=request.user).count()
        # except:
        #     tc = 0
        # print("tc check below")
        # print(tc)
        # if tc > 0:
        #     temp = Temp.objects.get(user=request.user)
        #     temp.delete()
        # temp =  Temp(user=request.user,order_id=order.id)
        # temp.save()
        mobile= request.user.phone
        key = send_otp(mobile)
        print(key)
        if key:
            obj = phoneOPTforoders(order_id=booking,user=request.user,otp=key)
            obj.save()
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.hospitalstaffdoctor.hospital.admin,booking=booking)
            notification.save()
        someones = ForSome.objects.filter(patient=request.user.patients )
        param = {'booking':booking,'someones':someones}
        return render(request,'patient/checkout.html',param)
            # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
            # res = conn.getresponse()
            # data = res.read()
            # data=data.decode("utf-8")
            # data=ast.literal_eval(data)
            # print(data)            
        #     return JsonResponse({'message' : 'success','status': True,'Booking_id':booking.id,"otp":key})
        # else:
        #     return JsonResponse({'message' : 'Error','status': False})

        # def new_method(self, now, booking):
        #     booking.reject_within_5__lt = now
    
   
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
    # temp= Temp.objects.get(user=request.user)
    # order = get_object_or_404(Orders,id=temp.order_id)
    # order.status=1
    # order.save()
    # book_for=order.booking_for
    # if book_for == "1":
    #     booking = get_object_or_404(Booking,id=order.bookingandlabtest)
    #     param ={'order':order,'booking':booking}
    # if book_for == "2":
    #     booking = get_object_or_404(Slot,id=order.bookingandlabtest)
    #     services = LabTest.objects.filter(slot=booking)
    #     param ={'order':order,'booking':booking,'services':services}
    # if book_for == "3":
    #     booking = get_object_or_404(PicturesForMedicine,id=order.bookingandlabtest)
    #     booking.amount_paid = True
    #     param ={'order':order,'booking':booking}
  
