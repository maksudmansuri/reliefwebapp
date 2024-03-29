from django.contrib import admin

from hospital.models import AmbulanceDetails, Blog, DoctorSchedule, HospitalStaffDoctorSchedual, HospitalStaffs,DepartmentPhones,Departments,RoomOrBadTypeandRates,ContactPerson,HospitalRooms,Insurances,HospitalMedias,HospitalTreatments,HospitalsPatients,HospitalServices,ServiceAndCharges, TimeSlot

# Register your models here.
 

admin.site.register(HospitalStaffs)
admin.site.register(HospitalStaffDoctorSchedual)
admin.site.register(Departments)
admin.site.register(RoomOrBadTypeandRates)
admin.site.register(HospitalRooms)
admin.site.register(ContactPerson)
admin.site.register(Insurances)
admin.site.register(DepartmentPhones)
admin.site.register(HospitalMedias)
admin.site.register(HospitalTreatments)
admin.site.register(HospitalsPatients)
admin.site.register(HospitalServices)
admin.site.register(ServiceAndCharges)
admin.site.register(AmbulanceDetails)
admin.site.register(Blog)
admin.site.register(TimeSlot)
admin.site.register(DoctorSchedule)