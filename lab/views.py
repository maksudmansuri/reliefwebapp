
from chat.models import Notification
from front.models import RatingAndComments
from patient.models import LabTest, NewLabTest, OrderBooking, Orders, Slot, TreatmentReliefPetient, phoneOPTforoders
from lab.models import HomeVisitCharges, LabSchedule, Medias
from hospital.models import DoctorSchedule, ServiceAndCharges, TimeSlot
from accounts.models import CustomUser, Labs, OPDTime
from django.contrib.messages.views import SuccessMessageMixin
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.contrib import messages
from datetime import datetime
import pytz
IST = pytz.timezone('Asia/Kolkata')
 
# Create your views here.

class LabDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        # try: 
        lab = Labs.objects.get(admin=request.user.id)
        showtime = datetime.now(tz=IST).date()
        print(showtime)
        bookings = OrderBooking.objects.filter(HLP=lab.admin,is_taken=False,is_active=True,is_cancelled = False,is_rejected = False)
        totalbookings = OrderBooking.objects.filter(HLP=lab.admin,is_taken=False,is_active=True,is_cancelled = False,is_rejected = False).count()
        booking_list = []
        for booking in bookings:
            newlabtest = NewLabTest.objects.filter(booking=booking)
            booking_list.append({'booking':booking,'labtest':newlabtest})
        bookings_now = OrderBooking.objects.filter(HLP=lab.admin,is_taken=False,is_active=True,is_cancelled = False,applied_date=showtime,is_rejected = False)
        todaybookings = OrderBooking.objects.filter(HLP=lab.admin,is_taken=False,is_active=True,is_cancelled = False,applied_date=showtime,is_rejected = False).count()
        booking_now_list = []
        for booking_now in bookings_now:
            newlabtest1 = NewLabTest.objects.filter(booking=booking_now)
            booking_now_list.append({'booking':booking_now,'labtest':newlabtest1})
        todaypayments = 1500
        # if hospital.hopital_name and hospital.about and hospital.address1 and hospital.city and hospital.pin_code and hospital.state and hospital.country and hospital.landline and hospital.registration_proof and hospital.profile_pic and hospital.establishment_year and hospital.registration_number and hospital.alternate_mobile and contacts:
            # contacts = HospitalPhones.objects.filter(hospital=hospital)
            # insurances = Insurances.objects.filter(hospital=hospital)
        # rooms = HospitalRooms.objects.filter(is_active=True,hospital=request.user.hospitals)
        param = {'booking_now_list':booking_now_list,'booking_list':booking_list,'totalbookings':totalbookings,'todaybookings':todaybookings,'todaypayments':todaypayments}
        
      
        # hospital = Hospitals.objects.get(admin=request.user.id)
        # contacts = HospitalPhones.objects.filter(hospital=hospital)
        # insurances = Insurances.objects.filter(hospital=hospital)

        # if hospital.hopital_name and hospital.about and hospital.address1 and hospital.city and hospital.pin_code and hospital.state and hospital.country and hospital.landline and hospital.registration_proof and hospital.profile_pic and hospital.establishment_year and hospital.registration_number and hospital.alternate_mobile and contacts:
        return render(request,"lab/index.html",param)
        
        
        # messages.add_message(request,messages.ERROR,"Some detail still Missing !")
        # param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
        # return render(request,"hospital/hospital_update.html",param)
       
        # def get(self,request):
        #     print("hello in m  in lab")
        #     return render(request,"lab/index.html")

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
    return HttpResponseRedirect(reverse("lab_home"))

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
        status = "OTP Verified"
         
        showtime = datetime.now(tz=IST)
        
        if postotp == str(key):  # Verifying the OTP
            apt.otp_verified_datetime = showtime
            apt.taken_date = showtime
            apt.status=status        
            apt.is_accepted=is_accepted    
            apt.is_otp_verified=is_otp_verified
            apt.save() 
            phoneotp.delete()        
            notification =  Notification(notification_type="1",from_user= request.user,to_user=apt.patient,booking=apt)
            notification.save()
            print(notification)
            messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
        else:
            messages.add_message(request,messages.ERROR,"OTP does not matched")
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
    return HttpResponseRedirect(reverse("lab_home"))

def UploadReportViews(request,id):
    report = request.FILES.get('report')        
    desc = request.POST.get('desc')
    # try:
    print(report)
    print(desc)
    print("out side if")
    booking = get_object_or_404(OrderBooking,id=id)
    if report:
        booking.report=report
        booking.status = "TAKEN"
        booking.is_report_uploaded =True
        booking.is_otp_verified = False
        booking.desc = desc
        booking.save()
        messages.add_message(request,messages.SUCCESS,"Report Successfully Uploaded")
    return HttpResponseRedirect(reverse("lab_home"))
    # except Exception as e:
    #     messages.add_message(request,messages.SUCCESS,e)
    #     return HttpResponseRedirect(reverse("lab_home"))

def dateleLabAppointment(request, id):
    booking = get_object_or_404(OrderBooking,id=id)
    labtests = NewLabTest.objects.filter(booking=booking)
    for labtest in labtests:
        labtest.is_active =False
        labtest.save()
    booking.is_active = False
    booking.save()
    messages.add_message(request,messages.SUCCESS,"Appointment Successfully Deleted")
    return HttpResponseRedirect(reverse("lab_home"))

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
    return HttpResponseRedirect(reverse("lab_home"))

class LabUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None 
        try:
            lab = Labs.objects.get(admin=request.user)
        except Exception as e:
            return HttpResponse(e)
        param={'lab':lab}
        return render(request,"lab/lab_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        lab_name = request.POST.get("lab_name")
        specialist = request.POST.get("specialist")
        profile_pic = request.FILES.get("profile_pic")

        about = request.POST.get("about")
        address = request.POST.get("address")
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
        # user creation Data
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        # mobile = request.POST.get("phone")
        alternate_mobile = request.POST.get("alternate_mobile")
        # email = request.POST.get("email")
        name_title = request.POST.get("name_title")

        #Schedule for Labs OPD and Appointment
        
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
        # if opening_time >= close_time and break_start_time >= close_time and break_end_time >= close_time and opening_time >= break_start_time  and opening_time >= break_end_time and break_start_time >= break_end_time:
        #     messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
        #     print(messages.error)
        #     return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id})) 

        print("we are indside a add hspitals")
        try:
            # opd = OPDTime.objects.get(user=request.user)
            # opd.delete()
            # opdtime= OPDTime(user=request.user,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            # opdtime.save()
            lab = Labs.objects.get(admin=request.user.id)
            lab.lab_name=lab_name
            lab.about=about
            lab.registration_number=registration_number
            lab.address=address
            lab.city=city
            lab.pin_code=pin_code
            lab.state=state
            lab.country=country
            lab.landline=landline

            if profile_pic:
                lab.profile_pic=profile_pic
                lab.admin.profile_pic=profile_pic

            print(registration_proof)
            if registration_proof:
               lab.registration_proof=registration_proof
            lab.establishment_year=establishment_year
            lab.alternate_mobile=alternate_mobile
            lab.website=website
            lab.linkedin=linkedin
            lab.facebook=facebook
            lab.instagram=instagram
            lab.twitter=twitter
            lab.is_appiled=True
            lab.is_verified=False
            lab.save()
            #edit customUSer
            lab.admin.first_name=first_name
            lab.admin.last_name=last_name
            lab.admin.name_title=name_title       
            lab.admin.save()           
                    
            
            print("All data saved")

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("lab_update"))

"""Reviews list and edit delete """
class LabReviewsListView(SuccessMessageMixin,ListView):
     def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.filter(HLP = request.user)
            total_review = RatingAndComments.objects.filter(HLP = request.user).count()
            print(review_list)
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"lab/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("lab_reviews")) 

"""
Lab new slot booking
"""

class LabScheduleCreateView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        lab = request.user.labs
        dates = LabSchedule.objects.filter(lab=lab).values('scheduleDate','id')
        schedule_dates ={item['scheduleDate'] for item in dates}
        schedule_dates_list = []
        for sch_Dat in schedule_dates:
            scd_type = LabSchedule.objects.filter(scheduleDate=sch_Dat,lab=lab).first()
            scd_type_all = LabSchedule.objects.filter(scheduleDate=sch_Dat,lab=lab)
            schedule_dates_list.append({'scd_type':scd_type,'sch_Dat':sch_Dat,'scd_type_all':scd_type_all})
            
            sch_type = LabSchedule.objects.values('scheduleDate','id')
        # print(schedule_dates_list)


        schedule_dates = LabSchedule.objects.filter()
        timeslots_15s = TimeSlot.objects.filter(schedule_type="15")
        timeslots_30s = TimeSlot.objects.filter(schedule_type="30")
        timeslots_45s = TimeSlot.objects.filter(schedule_type="45")
        timeslots_60s = TimeSlot.objects.filter(schedule_type="60")

        param = {'timeslots_15s':timeslots_15s,'timeslots_30s':timeslots_30s,'timeslots_45s':timeslots_45s,'timeslots_60s':timeslots_60s,'schedule_dates_list':schedule_dates_list}
       
        return render(request,'lab/view-lab-schedule.html',param)
    
    def post(self, request, *args, **kwargs):
        timeslot_list = request.POST.getlist('timeslot[]')
        print(timeslot_list)
        scheduleDate = request.POST.get('scheduleDate')
        print(scheduleDate)
        lab = request.user.labs
        labSchedules = LabSchedule.objects.filter(lab = lab)
        for doctorschedule in labSchedules:
            print(doctorschedule.scheduleDate)
            print(scheduleDate)
            if str(doctorschedule.scheduleDate) == str(scheduleDate):
                messages.add_message(request,messages.ERROR,"Already Booked date please delete if you want to change")
                return HttpResponseRedirect(reverse("manage_labschedule"))
        is_active =True
        for timeslot in timeslot_list:
            timeslot_obj = get_object_or_404(TimeSlot,id=timeslot)
            labschedule = LabSchedule(scheduleDate=scheduleDate,lab=lab,is_active=is_active,timeslot=timeslot_obj)
            labschedule.save()
        messages.add_message(request,messages.SUCCESS,"Suucessfully Created")
        return HttpResponseRedirect(reverse("manage_labschedule"))

def deleteTimeSlot(request,id):
    lab = request.user.labs
    date1 = LabSchedule.objects.get(lab=lab,id=id)
    dates = LabSchedule.objects.filter(lab=lab,scheduleDate=date1.scheduleDate)
    for date in dates:
        date.delete()
    messages.add_message(request,messages.SUCCESS,"Sucessfully Deleted")
    return HttpResponseRedirect(reverse("manage_labschedule"))

class ServicesViews(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        # try:
        lab = Labs.objects.get(admin=request.user)
        serviceandcharges = ServiceAndCharges.objects.filter(user=request.user,is_active=True)
        cnt =HomeVisitCharges.objects.filter(lab = lab,is_active=True).count()
        print(cnt)
        home = ""
        if cnt > 0:
            home = HomeVisitCharges.objects.get(lab = lab,is_active=True)
        # //except Exception as e:
        #     pass
        param={'lab':lab,'serviceandcharges':serviceandcharges,'home':home}
        return render(request,"lab/service_and_prices.html",param) 

    def post(self, request, *args, **kwargs):
        try:
            if request.method == "POST":
                service_name=request.POST.get('service_name')
                service_charge=request.POST.get('service_charge')
                print(service_charge)
              
                serviceandcharges = ServiceAndCharges(user=request.user,service_name=service_name,service_charge=service_charge,is_active=True)
                serviceandcharges.save()
                messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("add_lab_services"))

def HomeServicesViews(request):
    if request.method == "POST":
        service_charge = request.POST.get("service_charge")
        lab_id = request.POST.get("lab_id")
        lab = get_object_or_404(Labs,id=lab_id)
        serviceandcharges = HomeVisitCharges(charges=service_charge,is_active=True,lab=lab)
        serviceandcharges.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Added")
    return HttpResponseRedirect(reverse("add_lab_services"))

def HomeServicesUpdateViews(request):
    if request.method == "POST":
        homevisit_id = request.POST.get("homevisit_id")
        service_charge = request.POST.get("service_charge")
        print(service_charge)
        serviceandcharges = get_object_or_404(HomeVisitCharges,id=homevisit_id)
        serviceandcharges.charges=service_charge
        serviceandcharges.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
    return HttpResponseRedirect(reverse("add_lab_services"))

def UpdateServicesViews(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        id = request.POST.get("id")
        service_charge = request.POST.get("service_charge")
        serviceandcharges = get_object_or_404(ServiceAndCharges,id=id)
        serviceandcharges.service_name=service_name
        serviceandcharges.service_charge=service_charge
        serviceandcharges.save()
        messages.add_message(request,messages.SUCCESS,"Successfully Update")
    return HttpResponseRedirect(reverse("add_lab_services"))

def deleteServicesViews(request,id):
    service = service =get_object_or_404(ServiceAndCharges,id=id)
    service.is_active = False
    service.save()
    messages.add_message(request,messages.SUCCESS,"Successfully Delete")
    return HttpResponseRedirect(reverse("add_lab_services"))

class ManageMainGalleryView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            lab= get_object_or_404(Labs,admin=request.user)
            medias = Medias.objects.filter(lab=lab)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_main_gallery"))        
        param={'medias':medias}
        return render(request,"lab/manage_main_gallery.html",param)        

    def post(self, request, *args, **kwargs):
        media_type_list = request.POST.get('media_type')        
        media_content_list = request.FILES.getlist('media_content[]')        
        media_desc_list = request.POST.get('media_desc') 
        user= get_object_or_404(Labs,admin=request.user)
        print(media_type_list,media_content_list,media_desc_list,user)
        i=0
        for media_content in media_content_list:
            hospital_media = Medias(lab=user,media_type=media_type_list,media_desc=media_desc_list,media_content=media_content)
            hospital_media.is_active=True
            hospital_media.save() 
            i=i+1  
            print("Meida saved")      
        return HttpResponseRedirect(reverse("manage_main_gallery"))

def deleteMainGallery(request):
    if request.method == "POST":
        checked_list = request.POST.getlist("id[]")
        print(checked_list)
        for deletecheck in checked_list:
            hospital_media = Medias.objects.get(id=deletecheck)
            hospital_media.delete()
        messages.add_message(request,messages.SUCCESS,"Successfully gellery Deleted")
        return HttpResponseRedirect(reverse("manage_main_gallery"))

class ViewAppointmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            bookings = Slot.objects.filter(lab=request.user.labs,is_active=True,is_cancelled = False)
            booking_labtest_list =[] 
            for booking in bookings:
                labtest = LabTest.objects.filter(slot=booking)
                booking_labtest_list.append({'booking':booking,'labtest':labtest})
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("view_lab_appointment"))        
        param={'booking_labtest_list':booking_labtest_list}
        return render(request,"lab/manage_appointment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
        is_accepted = False
        is_taken = False
        is_rejected =False
        is_applied = False        
        try:
            booking = get_object_or_404(Slot, id=id)
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
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,slot=booking)
            notification.save()
            print(booking)
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(e)

def verifylabtestbooking(request):
    if request.POST:
        try:
            id = request.POST.get("slot_id")
            booking = Slot.objects.get(id=id)
            order = get_object_or_404(Orders,booking_for=2,bookingandlabtest=id)
            phoneotp = get_object_or_404(phoneOPTforoders, order_id = order)
            user = phoneotp.user #mobile is a user     
        
            postotp=request.POST.get("otp")
            
            showtime = datetime.now(tz=IST)
            key = phoneotp.otp  # Generating Key
            print(key)
            print(postotp)
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
                notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,slot=booking)
                notification.save()
                messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
            else:
                messages.add_message(request,messages.ERROR,"OTP does not matched")
            return HttpResponseRedirect(reverse("view_lab_appointment"))
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
           
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponse(e)  # False Call    
        


    
