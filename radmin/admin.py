from django.contrib import admin

from radmin.models import City, Country, State

# Register your models here.


admin.site.register(Country)
admin.site.register(City)
admin.site.register(State)