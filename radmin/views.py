from datetime import datetime
import pytz
from accounts.awsredirect import image
from discount.models import Campaign

from front.models import RatingAndComments
IST = pytz.timezone('Asia/Kolkata')
from django.contrib import messages
from django.contrib.auth import get_user_model
from patient.models import Booking, LabTest, OrderBooking, Orders, PicturesForMedicine, Slot, TreatmentReliefPetient, patientFile
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect, JsonResponse
from hospital.models import ContactPerson, HospitalMedias, HospitalStaffDoctorSchedual, HospitalsPatients, Insurances, ServiceAndCharges, TimeSlot
from accounts.models import CustomUser, HospitalDoctors, HospitalPhones, Hospitals, Labs, OPDTime, Patients, Pharmacy, Specailist
from django.shortcuts import get_object_or_404, render
from django.views.generic import View,CreateView,DetailView,DeleteView,ListView,UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.db.models import Q 

from radmin.models import City, Country, Disease, DonorRequest, State
# Create your views here.
   
class indexListView(ListView):
    model = Hospitals
    template_name = "radmin/newindex.html" 

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)  
        context["labs_list"] = Labs.objects.all() 
        context["pharmacy_list"] = Pharmacy.objects.all() 
        patients = Patients.objects.all()
        patients_list = []
        for patient in patients:
            total_apt =  OrderBooking.objects.filter(patient = patient.admin).count() 
            patients_list.append({'total_apt':total_apt,'patient':patient})
        context["patient_list"] = patients_list
        doctors = HospitalDoctors.objects.filter(is_hospital_added = False)
        # for doctor in doctors:
        #     total_apt =  OrderBooking.objects.filter(patient = patient.admin).count() 
        #     patients_list.append({'total_apt':total_apt,'patient':patient})
        context["hospitaldoctors_list"] = doctors
        return context
    
"""
Hospital Specialist Categories
"""
class AddHospitalSpecialistView(SuccessMessageMixin,CreateView):
    
    def get(self, request, *args, **kwargs):      
        speciallist=Specailist.objects.all()
        param={'speciallists':speciallist}
        return render(request,"radmin/specialities.html",param)
    
    def post(self, request, *args, **kwargs):
        specialist_name=request.POST.get("specialist_name")
        specialist_icon=request.FILES.get("specialist_icon")
        hover_icon=request.FILES.get("hover_icon")
        app_icon=request.FILES.get("app_icon")
        try:
            specailist = Specailist.objects.create(specialist_name=specialist_name)
            if specialist_icon:
                specailist.specialist_icon=specialist_icon
            if hover_icon:
                specailist.hover_icon=hover_icon           
            if app_icon:
                specailist.app_icon=app_icon           
            specailist.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
        messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        return HttpResponseRedirect(reverse("specialist_hospital")) 

def updateHospitalSpecialist(request,id):
    specialist_name=request.POST.get("specialist_name")
    specialist_icon=request.FILES.get("specialist_icon")
    hover_icon=request.FILES.get("hover_icon")
    app_icon=request.FILES.get("app_icon")
    
    try: 
        specailist = get_object_or_404(Specailist,id=id)
        specailist.specialist_name=specialist_name
     
        if specialist_icon:  
            specailist.specialist_icon=specialist_icon
        if hover_icon:
            specailist.hover_icon=hover_icon
        if app_icon:
            specailist.app_icon=app_icon   
        specailist.save()
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
    messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
    return HttpResponseRedirect(reverse("specialist_hospital")) 

def deleteHospitalSpecialist(request,id):
    specailist = get_object_or_404(Specailist,id=id)
    specailist.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("specialist_hospital")) 
 
"""
Hospitals All Views
"""

class HospitalallViews(ListView):
    model = Hospitals
    template_name = "radmin/hospital_all.html" 

def HospitalActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def HospitalDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def HospitalDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))

class hospitalUpdateViews(SuccessMessageMixin,UpdateView):
    UserModel=get_user_model()
    def get(self, request, *args, **kwargs):
        # hospital = None
        # contacts = None
        # insurances = None
        # try:
        id= kwargs['id']
        hospital = Hospitals.objects.get(id=id)
        contacts = HospitalPhones.objects.filter(hospital=hospital)
        insurances = Insurances.objects.filter(hospital=hospital)
        # opdtime=OPDTime.objects.get(user=request.user)
        specailists = Specailist.objects.all()
        print("hello")
        print(specailists)
        # except Exception as e:
            # return None
        param={'hospital':hospital,'insurances':insurances,'contacts':contacts,'specailists':specailists}
        return render(request,"radmin/doctor-profile-settings.html",param) 
    
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

       
        try:
            id=kwargs['id']
           
            hospital = Hospitals.objects.get(id=id)
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

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            # except:
            #     return render(request,"radmin/hospital_add.html") 
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)        
        return HttpResponseRedirect(reverse("radmin_home"))


"""
Patients All Views
"""

class PatientAllViews(ListView):
    model = Patients
    template_name = "radmin/patient_all.html" 

def PatientActivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def PatientDeactivate(request,id):
    hospital=Patients.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PatientDelete(request,id):
    hospital=Patients.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))

"""
Labs All Views
"""

class LabsAllViews(ListView):
    model = Labs
    template_name = "radmin/laboratory_all.html" 

def LabsActivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def LabsDeactivate(request,id):
    hospital=Labs.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})


def LabsDelete(request,id):
    hospital=Labs.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))

class LabUpdateViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None 
        id=kwargs['id']
        try:
            lab = Labs.objects.get(id=id)
        except Exception as e:
            return HttpResponse(e)  
        param={'lab':lab}
        return render(request,"radmin/lab_update.html",param) 
    
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

        print("we are indside a add hspitals")
        try:
            id=kwargs['id']
            lab = Labs.objects.get(id=id)
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
            
        return HttpResponseRedirect(reverse("radmin_home"))

"""Doctor Admin View"""
class DoctorUpdateViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None 
        id=kwargs['id']
        try:
            lab = HospitalDoctors.objects.get(id=id)
            specailists = Specailist.objects.all()      
        except Exception as e:
            return HttpResponse(e)  
        param={'hospital':lab,'specailists':specailists}
        return render(request,"radmin/doctor_update.html",param) 
    
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
            id=kwargs['id']
            hospital = HospitalDoctors.objects.get(id=id)
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
            

            messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
            
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            
        return HttpResponseRedirect(reverse("radmin_home"))

def DoctorsActivate(request,id):
    hospital=HospitalDoctors.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def DoctorsDeactivate(request,id):
    hospital=HospitalDoctors.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def DoctorDelete(request,id):
    hospital=HospitalDoctors.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))




"""
Pharmacy All Views
"""

class PharmacyAllViews(ListView):
    model = Pharmacy
    template_name = "radmin/pharmacy_all.html" 

def PharmacyActivate(request,id):
    hospital=Pharmacy.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("radmin_home"))

def PharmacyDeactivate(request,id):
    hospital=Pharmacy.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("radmin_home"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def PharmacyDelete(request,id):
    hospital=Pharmacy.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("radmin_home"))

class PharmacyUpdateViews(SuccessMessageMixin,UpdateView):
    def get(self, request, *args, **kwargs):
        # hospital = None
        # # contacts = None
        # # insurances = None
        # try:
        id=kwargs['id']
        pharmacy = Pharmacy.objects.get(id=id)
        opdtime=OPDTime.objects.get(user=pharmacy.admin)
            # insurances = Insurances.objects.filter(hospital=hospital)
        # except Exception as e:
        #     return HttpResponse(e)
        param={'pharmacy':pharmacy,'opdtime':opdtime}
        return render(request,"radmin/pharmacy_update.html",param) 
    
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
        print(opening_time1)
        break_end_time1 = request.POST.get("break_end_time")
        print(break_end_time1)
        break_start_time1 = request.POST.get("break_start_time")
        print(break_start_time1)
        close_time1 = request.POST.get("close_time")
        print(close_time1)

        opening_time = datetime.strptime(opening_time1,"%H:%M").time()
   
        close_time = datetime.strptime(close_time1,"%H:%M").time()
       
        break_start_time = datetime.strptime(break_start_time1,"%H:%M").time()
        
        break_end_time = datetime.strptime(break_end_time1,"%H:%M").time()
        id=kwargs['id']
        pharmacy = Pharmacy.objects.get(id=id)
        if Sunday is None and Monday is None and Tuesday is None and Wednesday is None and Thursday is None and Friday is None and Saturday is None:
            messages.add_message(request,messages.ERROR,"At least select one day")
            return HttpResponseRedirect(reverse("radmin_pharmacy_update", kwargs={'id':pharmacy.id}))
        if opening_time >= close_time and break_start_time >= close_time and break_end_time >= close_time and opening_time >= break_start_time  and opening_time >= break_end_time and break_start_time >= break_end_time:
            messages.add_message(request,messages.ERROR,"Time does not match kindly set Proper time ")
            print(messages.error)
           
            return HttpResponseRedirect(reverse("radmin_pharmacy_update", kwargs={'id':pharmacy.id})) 

        print("we are indside a add hspitals")
        try:
            print("inside pharmacy check")
            id=kwargs['id']
            pharmacy = Pharmacy.objects.get(id=id)
            opd = OPDTime.objects.get(user=pharmacy.admin)
            opd.delete()
            opdtime= OPDTime(user=pharmacy.admin,opening_time=opening_time,close_time=close_time,break_start_time=break_start_time,break_end_time=break_end_time,sunday=Sunday,monday=Monday,tuesday=Tuesday,wednesday=Wednesday,thursday=Thursday,friday=Friday,saturday=Saturday,is_active=True)
            opdtime.save()
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
            
        return HttpResponseRedirect(reverse("radmin_home"))
    
"""
Accident All Views
"""

class AccidentAllViews(ListView):
    model = Hospitals
    template_name = "radmin/accident_all.html" 

def AccidentActivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == False:
        hospital.is_verified=True
        hospital.is_appiled=False
        hospital.is_deactive=False
        hospital.save()
    # hospitals_list=Hospitals.objects.filter((Q(is_appiled=True) | Q(is_verified=True))  & Q(admin__is_active=True) & Q(admin__user_type=3))
    return HttpResponseRedirect(reverse("manage_accident_admin"))

def AccidentDeactivate(request,id):
    hospital=Hospitals.objects.get(id=id)
    if hospital is not None and hospital.is_verified == True:
        hospital.is_verified=False
        hospital.is_appiled=False
        hospital.is_deactive=True
        hospital.save()
    return HttpResponseRedirect(reverse("manage_accident_admin"))
    # return render(request,'counsellor/manage_student.html',{'hospitals_list':hospitals_list})

def AccidentDelete(request,id):
    hospital=Hospitals.objects.get(id=id)
    hospital.delete()
    return HttpResponseRedirect(reverse("manage_accident_admin"))


def hospitalUpdateView(request): 
    return render(request,"radmin/doctor_add.html")
 
def hospitalDeleteView(request): 
    return render(request,"radmin/doctor_add.html")

"""
Appointment all view
"""
class AppointmentListView(ListView):
    model = OrderBooking
    template_name = "radmin/appoinment.html"

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context["hos_apt"] = OrderBooking.objects.filter(booking_for = "H") 
        context["labs_apt"] = OrderBooking.objects.filter(booking_for = "L") 
        context["pharmacy_apt"] = OrderBooking.objects.filter(booking_for = "P") 
        context["doctor_apt"] = OrderBooking.objects.filter(booking_for = "D") 
        return context

class HosAppointmentAllViews(ListView):
    model = Booking
    template_name = "radmin/appointment_hospital_all.html"

class PhaAppointmentAllViews(ListView):
    model = PicturesForMedicine
    template_name = "radmin/appointment_pharmacy_all.html"
 
class LabsAppointmentAllViews(ListView):
    def get(self, request, *args, **kwargs):
        allslot = Slot.objects.filter(is_active=True)
        allslot_list = []
        for slots in allslot:
            labtest = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtest':labtest})
        param = {'allslot_list':allslot_list}
        return render(request,"radmin/appointment_labs_all.html",param)

"""
Profile of Hospital Labs Pharmacy Patient
"""
class HospitalDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hospital = get_object_or_404(Hospitals,admin__is_active=True,is_verified=True,is_deactive=False,id=hosital_id)
        doctors = HospitalDoctors.objects.filter(is_active=True,hospital=hospital)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
        hospitalstaffdoctor_list = []
        for hospitalstaffdoctor in doctors:
            hospitalstaffdoctorschedual = HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
            opd_time = []
            for dcsh in hospitalstaffdoctorschedual:
                if dcsh.work == "OPD":
                    shift = dcsh.shift
                    start_time = dcsh.start_time
                    end_time = dcsh.end_time
                opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
            hospitalstaffdoctor_list.append({'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time})
        param = {'hospital':hospital,'hospitalstaffdoctor_list':hospitalstaffdoctor_list,'hospitalservice':hospitalservice}  
        return render(request,"radmin/hospital_profile.html",param)

class DoctorsBookAppoinmentViews(SuccessMessageMixin,View):
    def get(self, request, *args, **kwargs):
        hosital_id=kwargs['id']
        hositaldcotorid_id=kwargs['did']
        hospital = get_object_or_404(Hospitals,is_verified=True,is_deactive=False,id=hosital_id)
        hospitalstaffdoctor = get_object_or_404(HospitalDoctors,is_active=True,id=hositaldcotorid_id)
        hospitalservice = ServiceAndCharges.objects.filter(user=hospital.admin)
      
        
        hospitalstaffdoctorschedual =HospitalStaffDoctorSchedual.objects.filter(hospitalstaffdoctor=hospitalstaffdoctor)
        opd_time = []
        for dcsh in hospitalstaffdoctorschedual:
            if dcsh.work == "OPD":
                shift = dcsh.shift
                start_time = dcsh.start_time
                end_time = dcsh.end_time
            opd_time.append({'shift':shift,'start_time':start_time,'end_time':end_time})
        
        param = {'hospital':hospital,'hospitalservice':hospitalservice,'hospitalstaffdoctor':hospitalstaffdoctor,'hospitalstaffdoctorschedual':hospitalstaffdoctorschedual,'opd_time':opd_time}  
        return render(request,"radmin/doctor_profile.html",param)
    
class LabDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        lab = get_object_or_404(Labs,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)
        services = ServiceAndCharges.objects.filter(user=lab.admin)        
        param = {'lab':lab,'services':services}  
        return render(request,"radmin/lab_profile.html",param)

class PharmacyDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        lab_id=kwargs['id']
        pharmacy = get_object_or_404(Pharmacy,admin__is_active=True,is_verified=True,is_deactive=False,id=lab_id)   

        param = {'pharmacy':pharmacy}  
        return render(request,"radmin/pharmacy_profile.html",param)

class PatientDetailsViews(DetailView):
    def get(self, request, *args, **kwargs):
        patient_id=kwargs['id']
        patient = get_object_or_404(Patients,admin__is_active=True,id=patient_id)
        slotbook = Slot.objects.filter(patient=patient.admin)
        allslot_list = []
        for slots in slotbook:
            labtests = LabTest.objects.filter(slot=slots)
            allslot_list.append({'slot':slots,'labtests':labtests})
        booking = Booking.objects.filter(patient=patient.admin) 

        param = {'patient':patient,'allslot_list':allslot_list,'booking':booking}  
        return render(request,"radmin/patient_profile.html",param)


"""
Add Location country state and city
"""
class AddCountriesView(SuccessMessageMixin,CreateView):
    
    def get(self, request, *args, **kwargs):      
        countries=Country.objects.all()
        states=State.objects.all()
        cities=City.objects.all()
        state_country_wise_list =[]
        for country in countries:
            state_list = State.objects.filter(country=country)
            state_country_wise_list.append({'country':country,'state_list':state_list})
        param={'countries':countries,'states':states,'cities':cities,'state_country_wise_list':state_country_wise_list}
        return render(request,"radmin/add-location.html",param)
    
    def post(self, request, *args, **kwargs):
        area = request.POST.get("area")
        if area == "country":
            country_name=request.POST.get("country_name")
            try:
                country = Country(country_name=country_name)
                country.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        if area == "state":
            state_name=request.POST.get("state_name")
            country=request.POST.get("country")
            print(country)
            country_name = get_object_or_404(Country,id=country)
            try:
                state = State(state_name=state_name,country=country_name)
                state.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        if area == "city":
            city_name=request.POST.get("city_name")
            state=request.POST.get("state")           
            # country=request.POST.get("country")
            # print(city_name,state,country)
            state_name = get_object_or_404(State,id=state) 
            country_name = get_object_or_404(Country,id=state_name.country.id)
            try:
                state = City(city_name=city_name,state=state_name,country=country_name)
                state.save()
            except Exception as e:
                messages.add_message(request,messages.ERROR,e)
            messages.add_message(request,messages.SUCCESS,"Succesfully Added")     
        return HttpResponseRedirect(reverse("loaction_area")) 

def deleteCountry(request,id):
    country = get_object_or_404(Country,id=id)
    country.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

def deleteState(request,id):
    state = get_object_or_404(State,id=id)
    state.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

def deleteCity(request,id):
    city = get_object_or_404(City,id=id)
    city.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("loaction_area")) 

class TimeSlotView(SuccessMessageMixin,CreateView):
    def get(self, request, *args, **kwargs):
        time_slots = TimeSlot.objects.all().order_by('schedule')
        timeslots_15s = TimeSlot.objects.filter(schedule_type="15")
        timeslots_30s = TimeSlot.objects.filter(schedule_type="30")
        timeslots_45s = TimeSlot.objects.filter(schedule_type="45")
        timeslots_60s = TimeSlot.objects.filter(schedule_type="60")
        print(timeslots_15s,timeslots_30s,timeslots_45s,timeslots_60s)
        param={'timeslots_15s':timeslots_15s,'timeslots_30s':timeslots_30s,'timeslots_45s':timeslots_45s,'timeslots_60s':timeslots_60s}
        return render(request,"radmin/time-slot.html",param)
 
    def post(self, request, *args, **kwargs):
        session = request.POST.get("session")
        schedule_type = request.POST.get("schedule_type")
        schedule = request.POST.get("schedule")
        schedule_check = TimeSlot.objects.filter(schedule=schedule,schedule_type=str(schedule_type)).count()
        if schedule_check > 0:
            messages.add_message(request,messages.ERROR,"Already Added Time..!")
            return HttpResponseRedirect(reverse("time_slot")) 
        time_slot = TimeSlot(session=str(session),schedule_type=schedule_type,schedule=schedule)
        time_slot.save()
        messages.add_message(request,messages.SUCCESS,"SuccessFully Added")
        return HttpResponseRedirect(reverse('time_slot'))

def deleteTimeSlot(request,id):
    time_slot = get_object_or_404(TimeSlot,id=id)
    time_slot.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("time_slot")) 


""" 
Reviews List 
"""

class ReviewsList(ListView):
    def get(self, request, *args, **kwargs):
        try:
            review_list = RatingAndComments.objects.all()
            total_review = RatingAndComments.objects.all().count()
            print(review_list)
            param={'review_list':review_list,'total_review':total_review}
            return render(request,"radmin/view_reviews.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No reviews Available")
            return HttpResponseRedirect(reverse("admin_reviews")) 


# def findState(request):
#     country_id = request.POST.get("country_id")
#     countries=Country.objects.all()
#     states=State.objects.all()
#     findstates=State.objects.filter(country=country_id)
#     cities=City.objects.all()
#     # param={'countries':countries,'states':states,'cities':cities,'findstates':findstates}
#     response = {'findstates':findstates}
#     return  HttpResponse(findstates)

"""RElief share view"""
def ReliefShare(request):
    # if request.method == "POST":
    id = request.POST.get("id")
    share = request.POST.get("share")
    page = request.POST.get("page")

    account = get_object_or_404(CustomUser,id=id)
    account.share = share
    account.save()
    messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
    return HttpResponseRedirect(reverse("radmin_home")) 
"""Donor Request List"""
class RequestForDonorListView(ListView):
    model = DonorRequest
    template_name = "radmin/request_donor.html"
    
"""Pateints Prfile And edit"""
class ReliefPatientViewsProfile(SuccessMessageMixin,DetailView):
     def get(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            patient=Patients.objects.get(id=id)
            # treatmentreliefpetient = TreatmentReliefPetient.objects.get(is_active=True,id=id)
            oldbooking = TreatmentReliefPetient.objects.filter(is_active=True,patient=patient)
            # hospitaldoctors = HospitalStaffDoctors.objects.filter(hospital=hospital,is_active=True)
            # serviceandcharges = ServiceAndCharges.objects.filter(user=hospital.admin)
            patientfiles = patientFile.objects.filter(patient=patient) 
            # slot = Slot.objects.filter(patient=treatmentreliefpetient.patient.admin) # yet not required
            # labtests =LabTest.objects.filter(slot__patient=treatmentreliefpetient.patient.admin,is_active=True,slot__send_to_doctor=True)
            # print(labtests)
            apts = OrderBooking.objects.filter(patient = patient.admin)
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
            return HttpResponseRedirect(reverse("manage_relief_patient"))        
        param={'apts':apts,'oldbooking':oldbooking,'patient':patient,'patientfiles':patientfiles}
        return render(request,"radmin/patient_profile.html",param)        
 
"""Lsit of All PAtients with hospital,docotr filter"""
class AdminAllPatientListView(ListView):
    def get(self, request, *args, **kwargs):
        try:
            hos=kwargs['id'] 
            hospital = get_object_or_404(Hospitals,admin=hos)           
            hospital_patient = Patients.objects.filter(hospital=hospital)
            chospital_patient = Patients.objects.filter(hospital=hospital).count()
            relief_patient = TreatmentReliefPetient.objects.filter(hospital=hospital)
            crelief_patient = TreatmentReliefPetient.objects.filter(hospital=hospital).count()

            param={'relief_patient':relief_patient,'chospital_patient':chospital_patient,'hospital_patient':hospital_patient,'crelief_patient':crelief_patient}
            return render(request,"radmin/patient_list.html",param)       
        except Exception as e:
            messages.add_message(request,messages.ERROR,"No Patients Available")
            return HttpResponseRedirect(reverse("radmin_home")) 

"""Disease Add Update Delete"""
class DiseaseListView(SuccessMessageMixin,CreateView):
    
    def get(self, request, *args, **kwargs):      
        diseases=Disease.objects.all()
        param={'diseases':diseases}
        return render(request,"radmin/diseases.html",param)
    
    def post(self, request, *args, **kwargs):
        name=request.POST.get("name")
        desc=request.POST.get("desc")
        d_icon=request.FILES.get("d_icon")
        print(desc)
        

        try:
            disease = Disease(name=name,desc=desc,is_active=True)
            if d_icon:
               disease.d_icon=d_icon
            disease.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
        messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        return HttpResponseRedirect(reverse("diseaselist")) 

def updateDisease(request,id):
    name=request.POST.get("name")
    desc=request.POST.get("desc")
    d_icon=request.FILES.get("d_icon")
    
    try: 
        disease = get_object_or_404(Disease,id=id)
        disease.name=name
        disease.desc=desc
        if d_icon:
            disease.d_icon=d_icon      
        disease.save()
    except Exception as e:
        messages.add_message(request,messages.ERROR,e)
    messages.add_message(request,messages.SUCCESS,"Succesfully Updated")
    return HttpResponseRedirect(reverse("diseaselist")) 

def deleteDisease(request,id):
    disease = get_object_or_404(Disease,id=id)
    disease.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("diseaselist")) 
 
 
class DiscountListView(SuccessMessageMixin,CreateView):    
    def get(self, request, *args, **kwargs):      
        discounts=Campaign.objects.all()
        specialist = Specailist.objects.all() 
        hospitals = Hospitals.objects.filter(admin__is_active= True,is_verified = True,is_deactive = False) 
        hospitaldoctors = HospitalDoctors.objects.filter(admin__is_active= True,is_verified = True,is_deactive = False, is_hospital_added = False) 
        labs = Labs.objects.filter(admin__is_active= True,is_verified = True,is_deactive = False) 
        pharmacy = Pharmacy.objects.filter(admin__is_active= True,is_verified = True,is_deactive = False) 
        param={'discounts':discounts,'pharmacy':pharmacy,'labs':labs,'hospitaldoctors':hospitaldoctors,'hospitals':hospitals,'specialist':specialist}
        return render(request,"radmin/discount.html",param)
    
    def post(self, request, *args, **kwargs):
        discount_rate=request.POST.get("discount_rate")
        # apply_to=request.POST.get("apply_to")
        target_specialist_list=request.POST.getlist("target_specialist []")
        target_hospital_list=request.POST.getlist("target_hospital []")
        target_hospitaldoctor_list=request.POST.getlist("target_hospitaldoctor []")
        target_lab_list=request.POST.getlist("target_lab []")
        target_pharmacy_list=request.POST.getlist("target_pharmacy []")
       
        try:
            all_campaign = Campaign.objects.all()
           
            #for specialist discount
            for target_specialist in target_specialist_list:
                spc = get_object_or_404(Specailist,id=target_specialist)                
                discount = Campaign(discount_rate = discount_rate,target_specialist=spc)           
                discount.save()
            #for target_hospital discount
            for target_hospital in target_hospital_list:
                hsp = get_object_or_404(Hospitals,id=target_hospital)
                for campaign in all_campaign:
                    if campaign.target_hospital == hsp:
                        messages.add_message(request,messages.ERROR,"Duplicate entry for  discount rate")
                        return HttpResponseRedirect(reverse("admin_discount"))
                discount = Campaign(discount_rate = discount_rate,target_hospital=hsp)           
                discount.save()
            # target_hospitaldoctor
            for target_hospitaldoctor in target_hospitaldoctor_list:
                hspdct = get_object_or_404(HospitalDoctors,id=target_hospitaldoctor)
                for campaign in all_campaign:
                    if campaign.target_hospitaldoctor == hspdct:
                        messages.add_message(request,messages.ERROR, "Duplicate entry for  discount rate ")
                        return HttpResponseRedirect(reverse("admin_discount"))
                discount = Campaign(discount_rate = discount_rate,target_hospitaldoctor=hspdct)           
                discount.save()
            for target_lab in target_lab_list:
                lb = get_object_or_404(Labs,id=target_lab)
                for campaign in all_campaign:
                    if campaign.target_lab == lb:
                        messages.add_message(request,messages.ERROR, "Duplicate entry for  discount rate ")
                        return HttpResponseRedirect(reverse("admin_discount"))
                discount = Campaign(discount_rate = discount_rate,target_lab=lb)           
                discount.save()
            for target_pharmacy in target_pharmacy_list:
                ph = get_object_or_404(Pharmacy,id=target_pharmacy)
                for campaign in all_campaign:
                    if campaign.target_pharmacy == ph:
                        messages.add_message(request,messages.ERROR, "Duplicate entry for  discount rate ")
                        return HttpResponseRedirect(reverse("admin_discount"))
                discount = Campaign(discount_rate = discount_rate,target_pharmacy=ph)           
                discount.save()
        except Exception as e:
            messages.add_message(request,messages.ERROR,e)
        messages.add_message(request,messages.SUCCESS,"Succesfully Added")
        return HttpResponseRedirect(reverse("admin_discount")) 

def DeleteDiscountView(request,id):
    disease = get_object_or_404(Campaign,id=id)
    disease.delete()
    messages.add_message(request,messages.SUCCESS,"Succesfully deleted")
    return HttpResponseRedirect(reverse("admin_discount")) 
 

