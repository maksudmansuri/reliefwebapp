from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin 
from django.urls import reverse
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,views_func,view_args,view_kwargs):
        modulename=views_func.__module__

        user=request.user
        if user.is_authenticated:
            # if user.force_to_psswd_chngd:
            #     if user.user_type == "4":
            #         user.force_to_psswd_chngd = False
            #         user.save()
            #         return HttpResponseRedirect('/password_change/')
            #     else:
            #         return HttpResponseRedirect('/password_change/')
            if user.user_type == "1":
                if modulename == "radmin.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "accounts.profilePic":
                    pass
                elif modulename == "media.views":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else: 
                    return HttpResponseRedirect(reverse("radmin_home"))
            elif user.user_type == "2":
                if modulename == "hospital.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("hospital_dashboard"))
            elif user.user_type == "3":
                if modulename == "doctor.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "accounts.profilePic":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "front.orderviews":
                    pass
                elif modulename == "media":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif  modulename == "chat.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("doctor_dashboard"))
            elif user.user_type == "4":
                if modulename == "patient.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "patient.PatientPassword":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif modulename == "media":
                    pass
                else:
                    # return redirect("/admin")
                    return HttpResponseRedirect(reverse("patient_home"))
            elif user.user_type == "5":
                if modulename == "lab.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "media":
                    pass
                else:
                    # return redirect("/admin")
                    return HttpResponseRedirect(reverse("lab_home"))
            elif user.user_type == "6":
                if modulename == "pharmacy.views" or modulename == "django.views.static":
                    pass
                elif modulename == "accounts.logoutview":
                    pass
                elif modulename == "front.views":
                    pass
                elif modulename == "django.contrib.auth.views":
                    pass
                elif modulename == "media":
                    pass
                else:
                    # return redirect("/admin")
                    return HttpResponseRedirect(reverse("pharmacy_home"))
            elif user.user_type == "0":
                # if modulename == "ecaadmin.views" or modulename == "django.views.static":
                #     pass
                # elif modulename == "front.views":
                #     pass
                # elif modulename == "media.views":
                #     pass
                # if modulename == "django.contrib.auth.views":
                #     pass
                # elif  modulename == "chat.views":
                #     pass
                # else:
                    # return HttpResponseRedirect(reverse("admin_home"))
                # if modulename == "django.contrib.auth.views":
                #     pass
                if modulename == "accounts.adminView":
                    pass
                elif modulename == "front.views":
                    pass
                print("admin")
                return HttpResponseRedirect(reverse('admin:index'))
                # else:
                    # return RedirectView.as_view(url=reverse_lazy('admin:index'))
                # return reverse('admin_login')
        else: 
            if request.path == reverse("dologin") or request.path == reverse("Authorizedsingup") or modulename == "front.views" or modulename == "accounts.views" or modulename == "django.views.static" or modulename == "django.contrib.auth.views" or modulename == "chat.views" or modulename == "accounts.api.views" or modulename == "front.api.views" or modulename == "allauth.account.views" or modulename == " allauth.socialaccount.views" or modulename == "patient.api.views" or request.path == reverse("schemas") or request.path == reverse("schema-swagger-ui") or request.path == reverse('schema-redoc'):
                pass
            else:
                next = request.path
                return HttpResponseRedirect(reverse("dologin")) or modulename == "allauth.account.views" or modulename == "front.views" or modulename == " allauth.socialaccount.views" or request.path == reverse("saccount") or modulename == "allauth.socialaccount.providers.oauth2.views"

