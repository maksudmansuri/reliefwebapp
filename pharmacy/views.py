from django.contrib.auth.models import User
from chat.models import Notification
from front.models import RatingAndComments
from lab.models import Medias
from patient.models import OrderBooking, Orders, PicturesForMedicine, phoneOPTforoders
from django.http.response import HttpResponse, HttpResponseRedirect
from accounts.models import CustomUser, OPDTime, Pharmacy
from django.contrib.messages.views import SuccessMessageMixin
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


class PharmaDashboardViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        # try: 
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            showtime = datetime.now(tz=IST).date()
            print(showtime)
            bookings = OrderBooking.objects.filter(HLP=pharmacy.admin,is_taken=False,is_active=True,is_cancelled = False,is_rejected = False)
            total_order = OrderBooking.objects.filter(HLP=pharmacy.admin,is_active=True,is_cancelled = False,is_rejected = False).count()
            bookings_now = OrderBooking.objects.filter(HLP=pharmacy.admin,is_taken=False,is_active=True,is_cancelled = False,applied_date=showtime,is_rejected = False)
            total_bookings_today = OrderBooking.objects.filter(HLP=pharmacy.admin,is_active=True,is_cancelled = False,applied_date=showtime,is_rejected = False).count()
            total_anount = 0
            for booking in bookings:
                total_anount = total_anount + booking.amount

            param = {'bookings':bookings,'bookings_now':bookings_now,'total_order':total_order,'total_bookings_today':total_bookings_today,'total_anount':total_anount}
            return render(request,"pharmacy/index.html",param)
            
         
            # messages.add_message(request,messages.ERROR,"Some detail still Missing !")
            # param={'hospital':hospital,'insurances':insurances,'contacts':contacts}
            # return render(request,"hospital/hospital_update.html",param)
       
    # def get(self,request):
    #     print("hello in m  in lab")
    #     return render(request,"lab/index.html")
class PharmaDashboardListViews(SuccessMessageMixin,ListView):
    def get(self, request, *args, **kwargs):
        # try: 
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            showtime = datetime.now(tz=IST).date()
            print(showtime)
            bookings = OrderBooking.objects.filter(HLP=pharmacy.admin,is_cancelled = False,is_rejected = False) 
            bookings_now = OrderBooking.objects.filter(HLP=pharmacy.admin,is_taken=False,is_active=True,is_cancelled = False,applied_date=showtime,is_rejected = False)
            booking_now_list = []
            param = {'bookings':bookings,'bookings_now':bookings_now}
            return render(request,"pharmacy/appointment_list.html",param)
 
def AcceptAPT(request,id): 
    try: 
        apt = get_object_or_404(OrderBooking,id=id,is_cancelled=False,is_active=True)
        is_applied = False        
        is_accepted = True
        status = "ACCEPTED"
        
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
            apt.store_invoice_uploaded = False
            apt.is_amount_paid = False
            apt.is_otp_verified=is_otp_verified
            apt.is_taken=True
            apt.save() 

            phoneotp.validated = True          
            phoneotp.save()    
            

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


class PharmacyUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None
        # try:
        pharmacy = Pharmacy.objects.get(admin=request.user.id)
        opdtime=OPDTime.objects.get(user=request.user)
            # insurances = Insurances.objects.filter(hospital=hospital)
        # except Exception as e:
        #     return HttpResponse(e)
        param={'pharmacy':pharmacy,'opdtime':opdtime}
        return render(request,"pharmacy/pharmacy_update.html",param) 
    
    def post(self, request, *args, **kwargs):
        pharmacy_name = request.POST.get("pharmacy_name")
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

        #Schedule for hospital OPD and Appointment
        
        Sunday = request.POST.get("Sunday")
        Monday = request.POST.get("Monday")
        Tuesday = request.POST.get("Tuesday")
        Wednesday = request.POST.get("Wednesday")
        Thursday = request.POST.get("Thursday")
        Friday = request.POST.get("Friday")
        Saturday = request.POST.get("Saturday")
        Sunday = request.POST.get("Sunday")
        opening_time1 = request.POST.get("opening_time")
        opening_time = datetime.strptime(opening_time1,"%H:%M").time()
        close_time1 = request.POST.get("close_time")
        close_time = datetime.strptime(close_time1,"%H:%M").time()
        break_start_time1 = request.POST.get("break_start_time")
        break_start_time = datetime.strptime(break_start_time1,"%H:%M").time()
        break_end_time1 = request.POST.get("break_end_time")
        break_end_time = datetime.strptime(break_end_time1,"%H:%M").time()
        if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
            messages.add_message(request,messages.ERROR,"At least select one day")
            return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id}))
        if opening_time >= close_time and break_start_time >= close_time and break_end_time >= close_time and opening_time >= break_start_time  and opening_time >= break_end_time and break_start_time >= break_end_time:
            messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
            print(messages.error)
            return HttpResponseRedirect(reverse("pharmacy_update", kwargs={'id':request.user.id})) 

        print("we are indside a add hspitals")
        try:
            
            opd = OPDTime.objects.get(user=request.user)
            opd.delete()
            opdtime= OPDTime(user=request.user,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            opdtime.save()
            pharmacy = Pharmacy.objects.get(admin=request.user.id)
            pharmacy.pharmacy_name=pharmacy_name
            pharmacy.about=about
            pharmacy.registration_number=registration_number
            pharmacy.address=address
            pharmacy.city=city
            pharmacy.pin_code=pin_code
            pharmacy.state=state
            pharmacy.country=country
            pharmacy.landline=landline

            if profile_pic:
                pharmacy.profile_pic=profile_pic
                pharmacy.admin.profile_pic=profile_pic

            print(registration_proof)
            if registration_proof:
                pharmacy.registration_proof=registration_proof
            pharmacy.establishment_year=establishment_year
            pharmacy.alternate_mobile=alternate_mobile
            pharmacy.website=website
            pharmacy.linkedin=linkedin
            pharmacy.facebook=facebook
            pharmacy.instagram=instagram
            pharmacy.twitter=twitter
            pharmacy.is_appiled=True
            pharmacy.is_verified=False
            pharmacy.save()
            #edit customUSer
            pharmacy.admin.first_name=first_name
            pharmacy.admin.last_name=last_name
            pharmacy.admin.name_title=name_title       
            pharmacy.admin.save()           
                    
            
            print("All data saved")

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("pharmacy_update"))
    
class ViewPharmacyAppointmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        try:
            picturesformedicine = PicturesForMedicine.objects.filter(pharmacy=request.user.pharmacy,is_active=True,is_cancelled = False)
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("view_pharmacy_appointment"))        
        param={'picturesformedicine':picturesformedicine}
        return render(request,"pharmacy/manage_appointment.html",param)        

    def post(self, request, *args, **kwargs):
        id = request.POST.get('a_id')        
        status = request.POST.get('status')
        print(id,status)
        is_accepted = False
        is_taken = False
        is_rejected =False
        is_applied = False        
        try:
            booking = PicturesForMedicine.objects.get(id=id)
            showtime = datetime.now(tz=IST)
            print(status)
        
            if status == 'accepted':
                is_accepted = True
                booking.accepted_date= showtime
            elif status == 'taken':
                is_taken= True
                booking.taken_date= showtime
                # treatmentreliefpetient = TreatmentReliefPetient(patient=booking.patient.patients,booking=booking,status="CHECKUPED",amount_paid=booking.service.service_charge,is_active=True)
                # treatmentreliefpetient.save()
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
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,picturesmedicine=booking)
            notification.save()
            return HttpResponse("ok")
        except Exception as e:
            return HttpResponse(e)

def verifypharmacybooking(request):
    if request.POST:
        try:
            id = request.POST.get("slot_id")
            booking = PicturesForMedicine.objects.get(id=id)
            order = get_object_or_404(Orders,booking_for=3,bookingandlabtest=id)
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
                notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,picturesmedicine=booking)
                notification.save()
                messages.add_message(request,messages.SUCCESS,"booking have been Verified Successfuly")
            else:
                messages.add_message(request,messages.ERROR,"OTP does not matched")
            return HttpResponseRedirect(reverse("view_pharmacy_appointment"))
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
            return HttpResponse(e)
    
def UpdloadInvoicePharmacy(request,id):
    store_invoice = request.FILES.get('store_invoice') 
    amount = request.POST.get('amount')   
    desc = request.POST.get('desc')
    try:
        booking = get_object_or_404(OrderBooking,id=id)
        if store_invoice:
            booking.store_invoice=store_invoice
            booking.amount=amount
            booking.status="AMOUNT_UPLOADED"
            booking.add_note = desc
            booking.store_invoice_uploaded=True
            showtime = datetime.now(tz=IST)
            booking.store_invoice_datetime=showtime
            print("here")
            print(booking.store_invoice_uploaded)
            booking.is_accepted =False
            booking.save()
            notification =  Notification(notification_type="1",from_user= request.user,to_user=booking.patient,booking=booking)
            notification.save()
            messages.add_message(request,messages.SUCCESS,"invoice Successfully Uploaded")
        return HttpResponseRedirect(reverse("pharmacy_home"))
    except Exception as e:
        messages.add_message(request,messages.SUCCESS,e)
        return HttpResponseRedirect(reverse("pharmacy_home"))

"""Reviews list and edit delete """
class PharmacyReviewsListView(SuccessMessageMixin,ListView):
     def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.filter(HLP = request.user)
            total_review = RatingAndComments.objects.filter(HLP = request.user).count()
            print(review_list)
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"pharmacy/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("pharmacy_reviews")) 


class ManageMainGalleryView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        try:
            user= get_object_or_404(Pharmacy,admin=request.user)
            medias = Medias.objects.filter(pharmacy=user)
        except Exception as e:
            messages.add_message(request,messages.ERROR,"user not available")
            return HttpResponseRedirect(reverse("manage_main_gallery"))        
        param={'medias':medias}
        return render(request,"pharmacy/manage_main_gallery.html",param)        

    def post(self, request, *args, **kwargs):
        media_type_list = request.POST.get('media_type')        
        media_content_list = request.FILES.getlist('media_content[]')        
        media_desc_list = request.POST.get('media_desc') 
        user= get_object_or_404(Pharmacy,admin=request.user)
        
        i=0
        for media_content in media_content_list:
            hospital_media = Medias(pharmacy=user,media_type=media_type_list,media_desc=media_desc_list,media_content=media_content)
            hospital_media.is_active=True
            hospital_media.save() 
            i=i+1  
            print("Meida saved")      
        return HttpResponseRedirect(reverse("pharmacy_manage_gallery"))

def deleteMainGallery(request):
    if request.method == "POST":
        checked_list = request.POST.getlist("id[]")
        print(checked_list)
        for deletecheck in checked_list:
            hospital_media = Medias.objects.get(id=deletecheck)
            hospital_media.delete()
        messages.add_message(request,messages.SUCCESS,"Successfully gellery Deleted")
        return HttpResponseRedirect(reverse("pharmacy_manage_gallery"))


def deleteServicesViews(request,id):
    booking = get_object_or_404(PicturesForMedicine,id=id)
    booking.is_active =False
    booking.save()
    messages.add_message(request,messages.SUCCESS,"Appointment Successfully Deleted")
    return HttpResponseRedirect(reverse("view_pharmacy_appointment"))

