
from decimal import Context
from typing import Counter
from django.contrib.messages import views
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import post_delete
from django.http import request, response
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls.base import reverse_lazy, translate_url
from django.views.generic.base import RedirectView, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from accounts import profilePic
from .models import CustomUser
from .EmailBackEnd import EmailBackEnd
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage, message
from django.conf import settings
from .utils import generate_token
import base64
from django.core.exceptions import ObjectDoesNotExist
from datetime import date, datetime, timedelta
import random
import http.client
import ast
conn = http.client.HTTPConnection("2factor.in")
# Create your views here.

def send_otp(phone):
    if phone:
        key = random.randint(999,9999)
        return key
    else:
        return False

    
# This class returns the string needed to generate the key
class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"

def verifyPhone(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone)
        print("inside virify phone")
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return render(request,"accounts/OTPVerification.html")  # False Call
    return render(request,"accounts/otp-verify.html",{'user':user})  #  Call

def resendOTP(request,phone):
    user = get_object_or_404(CustomUser,phone=phone)
    key = send_otp(phone)
    # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
    # print(OTP.at(user.counter))
    # otp=OTP.at(user.counter)
    # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(otp)+"&templatename=WomenMark1")
    # res = conn.getresponse()
    # data = res.read()
    # data=data.decode("utf-8")
    # data=ast.literal_eval(data)
    # print(data)
    # if data["Status"] == 'Success':
    #     user.otp_session_id = data["Details"]
    user.otp = str(key)
    user.save()
        # print('In validate phone :'+user.otp_session_id)
    messages.add_message(request,messages.SUCCESS,"OTP sent successfully") 
    return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

def verifyOTP(request,phone):
    try:
        user = CustomUser.objects.get(phone=phone) #mobile is a user
    except ObjectDoesNotExist:
        messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
        return HttpResponseRedirect(reverse("hospitalsingup"))  # False Call
    if request.POST:
        first=request.POST.get("first")
        second=request.POST.get("second")
        third=request.POST.get("third")
        forth=request.POST.get("forth")
        # fifth=request.POST.get("fifth")
        # sixth=request.POST.get("sixth")

        postotp = first+second+third+forth  #added in one string

        # keygen = generateKey()
        # key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        key =user.otp  # Generating Key
        # OTP = pyotp.HOTP(user.otp)  # HOTP Model
        #key = CustomUser.objects.get()
        # if OTP.verify(postotp, user.counter):  # Verifying the OTP
        if key == postotp:  # Verifying the OTP
            user.is_Mobile_Verified = True
            user.is_active=True
            user.save()
            messages.add_message(request,messages.SUCCESS,"Mobile Number is VArified Successfully")
        else:
            messages.add_message(request,messages.ERROR,"Incorrect OTP !")
            return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))
        #emila message for email verification
        current_site=get_current_site(request) #fetch domain    
        email_subject='Active your Account',
        message=render_to_string('accounts/activate.html',
        {
            'user':user,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        } #convert Link into string/message
        )
        print(message)
        email_message=EmailMessage(
            email_subject, 
            message,
            settings.EMAIL_HOST_USER,
            [user.email]
        )#compose email
        print(email_message)
        email_message.send() #send Email
        messages.add_message(request,messages.SUCCESS,"Sucessfully Singup Please Verify Your Account Email")
        if user is not None:
            if user.is_active == True:
                login(request,user)
                # request.session['logged in']=True
                if user.user_type=="1":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('radmin_home'))
                        # return HttpResponseRedirect(reverse('admin:index'))
                elif user.user_type=="2":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else: 
                        return HttpResponseRedirect(reverse('hospital_dashboard'))
                elif user.user_type=="3":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('doctor_dashboard'))
                elif user.user_type=="4":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    # print(" i am here but not goinf inside1")
                    # if user.profile_pic == None:
                    #     print(" i am here but not goinf inside2")
                    #     return HttpResponseRedirect(reverse('patientregisterstep1',kwargs={'user_id':user.id}))
                    # elif user.first_name == None:
                    #     print(" i am here but not goinf inside3")
                    #     return HttpResponseRedirect(reverse('patientregisterstep2',kwargs={'user_id':user.id}))
                    # elif user.patients.address == None:
                    #     print(" i am here but not goinf inside4")
                    #     return HttpResponseRedirect(reverse('patientregisterstep3',kwargs={'user_id':user.id}))
                    else:
                        return HttpResponseRedirect(reverse('patient_home'))
                elif user.user_type=="5":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('lab_home'))
                elif user.user_type=="6":
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('pharmacy_home'))
                else:
                # For Djnago default Admin Login 
                    return HttpResponseRedirect(reverse('admin:index'))
                    
                    # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                    # return HttpResponseRedirect(reverse('admin_home'))
            else:
                # message.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else: 
            # print(user.is_active)
            # messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
       
        # return HttpResponseRedirect(reverse("patientregisterstep1",kwargs={'user_id':user.id}))
        # return HttpResponseRedirect(reverse("dologin"))

def dologin(request):
    print(request.user)
    if request.method == "POST":
    #check user is authenticate or not
        user=EmailBackEnd.authenticate(request,username=request.POST.get("username"),password=request.POST.get("password"))
        if user is not None:
            if user.is_active == True:
                login(request,user)
                next = request.POST.get('next')
                # request.session['logged in']=True
                if user.user_type=="1":
                    if next:
                        return HttpResponseRedirect(next)
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('radmin_home'))
                        # return HttpResponseRedirect(reverse('admin:index'))
                elif user.user_type=="2":
                    if next:
                        return HttpResponseRedirect(next)
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else: 
                        return HttpResponseRedirect(reverse('hospital_dashboard'))
                elif user.user_type=="3": 
                    if next:
                        return HttpResponseRedirect(next)
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('doctor_dashboard'))
                elif user.user_type=="4":
                    print(next)
                    if next:
                        return HttpResponseRedirect(request.POST.get('next'))
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    # print("hello",user.profile_pic,user.first_name,user.patients.address)
                    # if user.profile_pic is None:
                    #     return HttpResponseRedirect(reverse("patientregisterstep1",kwargs={'user_id':user.id}))
                    # elif user.first_name is None:
                    #     return HttpResponseRedirect(reverse('patientregisterstep2',kwargs={'user_id':user.id}))
                    # elif user.patients.address is None:
                    #     return HttpResponseRedirect(reverse('patientregisterstep3',kwargs={'user_id':user.id}))
                    else:
                        return HttpResponseRedirect(reverse('front_home'))
                elif user.user_type=="5":
                    if next:
                        return HttpResponseRedirect(next)
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('lab_home'))
                elif user.user_type=="6":
                    if next:
                        return HttpResponseRedirect(next)
                    # elif user.profile_pic:
                    #     return HttpResponseRedirect(reverse('profile_picUpload'))
                    else:
                        return HttpResponseRedirect(reverse('pharmacy_home'))
                else:
                # For Djnago default Admin Login 
                    return HttpResponseRedirect(reverse('admin:index'))
                    
                    # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                    # return HttpResponseRedirect(reverse('admin_home'))
            else:
                # message.add_message(request,messages.ERROR,"Please Verify Your Account First")
                return redirect('/accounts/dologin')
        else: 
            # print(user.is_active)
            # messages.add_message(request,messages.ERROR,"User Not Found you haved to Register First")
            return redirect("dologin")
    return render(request,'accounts/login.html')
       
class HospitalSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/hospitalsingupnew.html"
    model=CustomUser 
    fields=["email","phone","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=2
        user.username=form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        #key = base64.b32encode((send_otp(mobile).encode()))
        # key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        key = send_otp(mobile)
        # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        # print(OTP.at(user.counter))
        # otp=OTP.at(user.counter)
        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(otp)+"&templatename=WomenMark1")
        # res = conn.getresponse()
        # data = res.read()
        # data=data.decode("utf-8")
        # data=ast.literal_eval(data)
        # print(data)
        # if data["Status"] == 'Success':
        #     user.otp_session_id = data["Details"]
        user.otp = str(key)
        user.save()
            # print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP has been sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))
        # else:
        #     messages.add_message(self.request,messages.ERROR,"OTP sending Failed") 
        #     return HttpResponseRedirect(reverse("hospitalsingup"))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        
        # return HttpResponseRedirect(reverse("OTP_Gen",kwargs={"user":user.phone}))  # send to next page with OTP

class DoctorSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/doctorsingup.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Doctor User
        print('i m here at dosignup')
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.username=form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        key = send_otp(mobile)
        user.otp = str(key)
        user.hospitaldoctors.is_hospital_added = False 
        user.save()
        messages.add_message(self.request,messages.SUCCESS,"OTP has been sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

class PatientSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/patientsingupnew.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "Patient Account Created" 
 
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.user_type=4
        user.username=form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        user.counter += 1  # Update Counter At every Call
        user.is_active= True
        user.save() # Save the data
        mobile= user.phone
        key = send_otp(mobile)
        print("i am here")
        # keygen = generateKey()
        # key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        # key = base64.b32encode((send_otp(mobile).encode()))
        # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        # print(OTP.at(user.counter))
        # otp=OTP.at(user.counter)
        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
        # res = conn.getresponse()
        # data = res.read()
        # data=data.decode("utf-8")
        # data=ast.literal_eval(data)
        # print(data)
        # if data["Status"] == 'Success':
        #     user.otp_session_id = data["Details"]
        user.otp = str(key)
        user.save()
            # print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP has been sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

class PatientSingupStep1(UpdateView):
    def get(self, request, *args, **kwargs) :
        user_id=kwargs['user_id']
        user = get_object_or_404(CustomUser,id=user_id)
        param = {'user':user}
        return render(request,"accounts/patient-register-step1.html",param)

    def post(self, request, *args, **kwargs) :
        user_id=kwargs['user_id']
        user = get_object_or_404(CustomUser,id=user_id)
        profile_pic = request.FILES.get("profile_pic")
        if profile_pic:
            fs=FileSystemStorage()
            filename1=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename1)
            user.profile_pic=profile_pic_url
            user.save()
            user.patients.profile_pic=profile_pic_url
            user.patients.save()
        else:
            messages.add_message(request,messages.SUCCESS,"Profile ppictureic not uploaded")
            return HttpResponseRedirect(reverse("patientregisterstep1",kwargs={'user_id':user.id}))
        messages.add_message(request,messages.SUCCESS,"Sucessfully uploaded profile picture")
        return HttpResponseRedirect(reverse("patientregisterstep2",kwargs={'user_id':user.id}))

class PatientSingupStep2(UpdateView):
    def get(self, request, *args, **kwargs) :
        user_id=kwargs['user_id']
        user = get_object_or_404(CustomUser,id=user_id)
        param = {'user':user}
        return render(request,"accounts/patient-register-step2.html",param)
    
    def post(self, request, *args, **kwargs) :
        user_id=kwargs['user_id'] 
        user = get_object_or_404(CustomUser,id=user_id)
        name_title = request.POST.get('name_title')
        fisrt_name = request.POST.get('fisrt_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        bloodgroup = request.POST.get('bloodgroup')
        age1 = (date.today() - datetime.strptime(dob, "%Y-%m-%d").date()) // timedelta(days=365.2425)
        print(user,name_title,fisrt_name,last_name,gender,dob,bloodgroup,age1)
        
        user.patients.name_title=name_title
        user.name_title = name_title
        user.first_name = fisrt_name
        user.last_name = name_title
        # user.patients.name_title=name_title
        user.patients.fisrt_name=fisrt_name
        user.patients.last_name=last_name
        user.patients.gender=gender
        user.patients.dob=dob
        user.patients.bloodgroup=bloodgroup
        user.patients.age=age1
        user.patients.save()
        user.save()      
        
            # messages.add_message(request,messages.SUCCESS,"Profile pictureic not uploaded")
            # return HttpResponseRedirect(reverse("patientregisterstep2",kwargs={'user_id':user.id}))
        messages.add_message(request,messages.SUCCESS,"Sucessfully uploaded profile picture")
        return HttpResponseRedirect(reverse("patientregisterstep3",kwargs={'user_id':user.id}))

class PatientSingupStep3(UpdateView):
    def get(self, request, *args, **kwargs) :
        user_id=kwargs['user_id']
        user = get_object_or_404(CustomUser,id=user_id)
        param = {'user':user}
        
        return render(request,"accounts/patient-register-step3.html",param)
    
    def post(self, request, *args, **kwargs) :
        user_id=kwargs['user_id'] 
        user = get_object_or_404(CustomUser,id=user_id)
        alternate_mobile = request.POST.get('alternate_mobile')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_Code = request.POST.get('zip_Code') 
        state = request.POST.get('state')
        country = request.POST.get('country')
        if alternate_mobile == None or address == None or city == None or zip_Code == None or  state == None or country == None:
            user.patients.alternate_mobile=alternate_mobile
            user.patients.address=address
            user.patients.city=city
            user.patients.state=state
            user.patients.zip_Code=zip_Code
            user.patients.country=country
            user.patients.save()
        else:
            messages.add_message(request,messages.SUCCESS,"Profile pictureic not uploaded")
            return HttpResponseRedirect(reverse("patientregisterstep3",kwargs={'user_id':user.id}))
        messages.add_message(request,messages.SUCCESS,"Sucessfully uploaded profile picture")
        return HttpResponseRedirect(reverse('patient_home'))

# class PatientSingupStep4(UpdateView):
#     def get(self, request, *args, **kwargs) :
#         user_id=kwargs['user_id']
#         user = get_object_or_404(CustomUser,id=user_id)
#         param = {'user':user}
#         return render(request,"accounts/patient-register-step4.html",param)

# class PatientSingupStep5(UpdateView):
#     def get(self, request, *args, **kwargs) :
#         user_id=kwargs['user_id']
#         user = get_object_or_404(CustomUser,id=user_id)
#         param = {'user':user}
#         return render(request,"accounts/patient-register-step5.html",param)

class AuthorizedSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/athorizationsnew.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "Admin User Created" 

    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=1
        user.is_active=True
        user.username=form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.save() # Save the data
        return HttpResponseRedirect(reverse("dologin"))
 
class LabSingup(SuccessMessageMixin,CreateView):
    template_name="accounts/labsingupnew.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "LAB User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('I am here at LAB singup')
        user=form.save(commit=False)
        user.user_type=5
        user.username=form.cleaned_data["email"]    
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        # keygen = generateKey()
        # key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        key = send_otp(mobile)
        print(key)
        # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        # print(OTP.at(user.counter))
        # otp=OTP.at(user.counter)
        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
        # res = conn.getresponse()
        # data = res.read()
        # data=data.decode("utf-8")
        # data=ast.literal_eval(data)
        # print(data)
        # if data["Status"] == 'Success':
        #     user.otp_session_id = data["Details"]
        user.otp = str(key)
        user.save()
        #     print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

class PharmacySingup(SuccessMessageMixin,CreateView):
    template_name="accounts/pharmacysingupnew.html"
    model=CustomUser
    fields=["email","phone","password"]
    success_message = "Hospital User Created"  
    def form_valid(self,form):
        #Saving Custom User Object for Merchant User
        print('i m here at Hospital singup')
        user=form.save(commit=False)
        user.user_type=6
        user.username=form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        print('just one step ahead save?')   
        user.counter += 1  # Update Counter At every Call
        user.save() # Save the data
        mobile= user.phone
        key = send_otp(mobile)
        # key = base64.b32encode(keygen.returnValue(mobile).encode())  # Key is generated
        
        # OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        # print(OTP.at(user.counter))
        # otp=OTP.at(user.counter)
        # conn.request("GET", "https://2factor.in/API/R1/?module=SMS_OTP&apikey=f08f2dc9-aa1a-11eb-80ea-0200cd936042&to="+str(mobile)+"&otpvalue="+str(key)+"&templatename=WomenMark1")
        # res = conn.getresponse()
        # data = res.read()
        # data=data.decode("utf-8")
        # data=ast.literal_eval(data)
        # print(data)
        # if data["Status"] == 'Success':
        #     user.otp_session_id = data["Details"]
        user.otp = str(key)
        user.save()
        # print('In validate phone :'+user.otp_session_id)
        messages.add_message(self.request,messages.SUCCESS,"OTP sent successfully") 
        return HttpResponseRedirect(reverse("verifyPhone",kwargs={'phone':user.phone}))

def adminSingup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        r=CustomUser.objects.filter(username=username)
        if r.count():
            msg=messages.error(request,"Username  Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))

        email = request.POST.get('email')
        e=CustomUser.objects.filter(email=email)
        if e.count():        
            msg=messages.error(request,"Email Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
            
        phone = request.POST.get('phone')
        p=CustomUser.objects.filter(phone=phone)
        if p.count():
            msg=messages.error(request,"Phone Already Exits")
            return HttpResponseRedirect(reverse("dosingup"))
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password2 and password1 != password2:
            msg=messages.error(request,"Password Does Match")
            return HttpResponseRedirect(reverse("dosingup"))
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        print('i m here at dosignup')
        print(email,first_name,last_name,username,phone,password1)
        user=CustomUser.objects.create_user(username=username,password=password1,email=email)
        # user.save(commit=False)
        print('first name ')
        user.last_name = last_name
        print('last name ')
        user.phone=phone
        user.user_type="2"
        print('first name lats name nad phone done')
        user.first_name = first_name
        user.save()
        print('i m done my dosignup')
        # current_site=get_current_site(request)
        # email_subject='Active your Account',
        # message=render_to_string('accounts/activate.html',
        # {
        #     'user':user,
        #     'domain':current_site.domain,
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk/tt)),
        #     'token':generate_token.make_token(user)
        # }
        # )
        # print(urlsafe_base64_encode(force_bytes(user.pk)),)
        # print(generate_token.make_token(user))
        # print(current_site.domain)
        # email_message=EmailMessage(
        #     email_subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [email]
        # )
        # email_message.send()
        # msg=messages.success(request,"Sucessfully Singup Please Verify Your Account First")
        print("hello bhia ahiya ayo em")           
        return HttpResponseRedirect(reverse("dologin"))
        # except:
        #     msg=messages.error(request,"Connection Error Try Again")
        #     return HttpResponseRedirect(reverse("dosingup"))
    return render(request,"accounts/dosingup.html")

def activate(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user=CustomUser.objects.get(pk=uid) 
    except:
        user=None
    if user is not None and generate_token.check_token(user,token):
        if user.is_Mobile_Verified:
            user.is_active=True
        user.is_Email_Verified=True
        user.save()
        messages.add_message(request,messages.SUCCESS,'account  is Activated Successfully')
        return HttpResponseRedirect(reverse('dologin'))
    return render(request,'accounts/activate_failed.html',status=401)

# def VerifyOTP(request,phone):
#     try:
#         Mobile = CustomUser.objects.get(phone=phone)
#     except ObjectDoesNotExist:
#         messages.add_message(request,messages.ERROR,"Mobile number does not Exits")
#         return HttpResponseRedirect(reverse("OTP_Gen"))  # False Call
#     if request.POST:
#         pass
#     keygen = generateKey()
#     key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
#     OTP = pyotp.HOTP(key)  # HOTP Model
#     if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
#         Mobile.is_Mobile_Verified = True
#         if Mobile.is_Email_Verified:
#             Mobile.is_active=True
#         Mobile.save()
#         messages.add_message(request,messages.ERROR,"Mobile Verified Successfuly")
#     return HttpResponseRedirect(reverse("dologin"))

def FourZeroFour(request):
    return render(request ,'accounts/error-404.html',)


def logout_view(request):
    logout(request)
    return redirect('dologin')