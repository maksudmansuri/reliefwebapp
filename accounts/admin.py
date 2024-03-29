from django.contrib import admin
from accounts.models import CustomUser,HospitalDoctors, HospitalPhones, AdminHOD, Hospitals, Labs, OPDTime, Patients, Pharmacy, PhoneOTP, Specailist, UserPayments
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, AuthorAdmin)
admin.site.register(HospitalDoctors)
admin.site.register(Patients)
admin.site.register(AdminHOD)
admin.site.register(HospitalPhones)
admin.site.register(Hospitals)
admin.site.register(PhoneOTP)
admin.site.register(Labs)
admin.site.register(Pharmacy)
admin.site.register(UserPayments)
admin.site.register(OPDTime)
admin.site.register(Specailist)
