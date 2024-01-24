from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "employee_management_app.HodViews" or modulename == "django.views.static":
                    pass
                elif modulename == "employee_management_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "employee_management_app.ManagerViews" or modulename == "django.views.static" or modulename == "employee_management_app.EditResultViewClass":
                    pass
                elif modulename == "employee_management_app.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("manager_home"))
            elif user.user_type == "3":
                if modulename == "employee_management_app.EmployeeViews" or modulename == "django.views.static":
                    pass
                elif modulename == "employee_management_app.views":
                    pass    
                else:
                    return HttpResponseRedirect(reverse("employee_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))
            