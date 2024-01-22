import json

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from employee_management_app.forms import AddEmployeeForm, EditEmployeeForm
from employee_management_app.models import CustomUser, Managers, Departments, Roles, Employees, SessionYearModel, LeaveReportEmployee, Attendance, AttendanceReport


def admin_home(request):
    employee_count = Employees.objects.all().count()
    manager_count = Managers.objects.all().count()
    role_count = Roles.objects.all().count()
    department_count = Departments.objects.all().count()

    department_all = Departments.objects.all()
    department_name_list = []
    role_count_list = []
    employee_count_list_in_department = []
    for department in department_all:
        roles = Roles.objects.filter(department_id=department.id).count()
        employees = Employees.objects.filter(department_id=department.id).count()
        department_name_list.append(department.department_name)
        role_count_list.append(roles)
        employee_count_list_in_department.append(employees)

    roles_all = Roles.objects.all()
    role_list = []
    employee_count_list_in_role = []
    for role in roles_all:
        department = Departments.objects.get(id=role.department_id.id)
        employee_count = Employees.objects.filter(department_id=department.id).count()
        role_list.append(role.role_name)
        employee_count_list_in_role.append(employee_count)

    managers = Managers.objects.all()
    attendance_present_list_managers = []
    attendance_absent_list_managers = []
    manager_name_list = []
    for manager in managers:
        role_ids = Roles.objects.filter(manager_id=manager.admin.id)
        attendance = Attendance.objects.filter(role_id__in=role_ids).count()
        leaves = LeaveReportManagers.objects.filter(manager_id=manager.id, leave_status=1).count()
        attendance_present_list_managers.append(attendance)
        attendance_absent_list_managers.append(leaves)
        manager_name_list.append(manager.admin.username)

    employees_all = Employees.objects.all()
    attendance_present_list_employees = []
    attendance_absent_list_employees = []
    employee_name_list = []
    for employee in employees_all:
        attendance = AttendanceReport.objects.filter(employee_id=employee.id, status=True).count()
        absent = AttendanceReport.objects.filter(employee_id=employee.id, status=False).count()
        leaves = LeaveReportEmployee.objects.filter(employee_id=employee.id, leave_status=1).count()
        attendance_present_list_employees.append(attendance)
        attendance_absent_list_employees.append(leaves + absent)
        employee_name_list.append(employee.admin.username)

    return render(request, "hod_template/home_content.html",
                  {"employee_count": employee_count, "manager_count": manager_count, "role_count": role_count,
                   "department_count": department_count, "department_name_list": department_name_list,
                   "role_count_list": role_count_list, "employee_count_list_in_department": employee_count_list_in_department,
                   "employee_count_list_in_role": employee_count_list_in_role, "role_list": role_list,
                   "manager_name_list": manager_name_list,
                   "attendance_present_list_managers": attendance_present_list_managers,
                   "attendance_absent_list_managers": attendance_absent_list_managers,
                   "employee_name_list": employee_name_list,
                   "attendance_present_list_employees": attendance_present_list_employees,
                   "attendance_absent_list_employees": attendance_absent_list_employees})


def add_manager(request):
    return render(request, "hod_template/add_manager_template.html")


def add_manager_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                                  first_name=first_name, user_type=2)
            user.managers.address = address
            user.save()
            messages.success(request, "Successfully Added Manager")
            return HttpResponseRedirect(reverse("add_manager"))
        except:
            messages.error(request, "Failed to Add Manager")
            return HttpResponseRedirect(reverse("add_manager"))


def add_department(request):
    return render(request, "hod_template/add_department_template.html")


def add_department_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        department = request.POST.get("department")
        try:
            department_model = Departments(department_name=department)
            department_model.save()
            messages.success(request, "Successfully Added Department")
            return HttpResponseRedirect(reverse("add_department"))
        except Exception as e:
            print(e)
            messages.error(request, "Failed To Add Department")
            return HttpResponseRedirect(reverse("add_department"))


def add_employee(request):
    form = AddEmployeeForm()
    return render(request, "hod_template/add_employee_template.html", {"form": form})


def add_employee_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        form = AddEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]
            department_id = form.cleaned_data["department"]
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)

            try:
                user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                      last_name=last_name, first_name=first_name, user_type=3)
                user.employees.address = address
                department_obj = Departments.objects.get(id=department_id)
                user.employees.department_id = department_obj
                user.employees.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Added Employee")
                return HttpResponseRedirect(reverse("add_employee"))
            except:
                messages.error(request, "Failed to Add Employee")
                return HttpResponseRedirect(reverse("add_employee"))
        else:
            form = AddEmployeeForm(request.POST)
            return render(request, "hod_template/add_employee_template.html", {"form": form})


def add_role(request):
    departments = Departments.objects.all()
    return render(request, "hod_template/add_role_template.html", {"departments": departments})


def add_role_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        role_name = request.POST.get("role_name")
        department_id = request.POST.get("department")
        department = Departments.objects.get(id=department_id)

        try:
            role = Roles(role_name=role_name, department_id=department)
            role.save()
            messages.success(request, "Successfully Added Role")
            return HttpResponseRedirect(reverse("add_role"))
        except:
            messages.error(request, "Failed to Add Role")
            return HttpResponseRedirect(reverse("add_role"))


def manage_manager(request):
    managers = Managers.objects.all()
    return render(request, "hod_template/manage_manager_template.html", {"managers": managers})


def manage_employee(request):
    employees = Employees.objects.all()
    return render(request, "hod_template/manage_employee_template.html", {"employees": employees})


def manage_department(request):
    departments = Departments.objects.all()
    return render(request, "hod_template/manage_department_template.html", {"departments": departments})


def manage_role(request):
    roles = Roles.objects.all()
    return render(request, "hod_template/manage_role_template.html", {"roles": roles})


def edit_manager(request, manager_id):
    manager = Managers.objects.get(admin=manager_id)
    return render(request, "hod_template/edit_manager_template.html", {"manager": manager, "id": manager_id})


def edit_manager_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        manager_id = request.POST.get("manager_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        address = request.POST.get("address")

        try:
            user = CustomUser.objects.get(id=manager_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            manager_model = Managers.objects.get(admin=manager_id)
            manager_model.address = address
            manager_model.save()
            messages.success(request, "Successfully Edited Manager")
            return HttpResponseRedirect(reverse("edit_manager", kwargs={"manager_id": manager_id}))
        except:
            messages.error(request, "Failed to Edit Manager")
            return HttpResponseRedirect(reverse("edit_manager", kwargs={"manager_id": manager_id}))


def edit_employee(request, employee_id):
    request.session['employee_id'] = employee_id
    employee = Employees.objects.get(admin=employee_id)
    form = EditEmployeeForm()
    form.fields['email'].initial = employee.admin.email
    form.fields['first_name'].initial = employee.admin.first_name
    form.fields['last_name'].initial = employee.admin.last_name
    form.fields['username'].initial = employee.admin.username
    form.fields['address'].initial = employee.address
    form.fields['department'].initial = employee.department_id.id
    form.fields['sex'].initial = employee.gender
    form.fields['session_year_id'].initial = employee.session_year_id.id
    return render(request, "hod_template/edit_employee_template.html",
                  {"form": form, "id": employee_id, "username": employee.admin.username})


def edit_employee_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id = request.session.get("employee_id")
        if employee_id == None:
            return HttpResponseRedirect(reverse("manage_employee"))

        form = EditEmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_year_id = form.cleaned_data["session_year_id"]
            department_id = form.cleaned_data["department"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                user = CustomUser.objects.get(id=employee_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()

                employee = Employees.objects.get(admin=employee_id)
                employee.address = address
                session_year = SessionYearModel.object.get(id=session_year_id)
                employee.session_year_id = session_year
                employee.gender = sex
                department = Departments.objects.get(id=department_id)
                employee.department_id = department
                if profile_pic_url != None:
                    employee.profile_pic = profile_pic_url
                employee.save()
                del request.session['employee_id']
                messages.success(request, "Successfully Edited Employee")
                return HttpResponseRedirect(reverse("edit_employee", kwargs={"employee_id": employee_id}))
            except:
                messages.error(request, "Failed to Edit Employee")
                return HttpResponseRedirect(reverse("edit_employee", kwargs={"employee_id": employee_id}))
        else:
            form = EditEmployeeForm(request.POST)
            employee = Employees.objects.get(admin=employee_id)
            return render(request, "hod_template/edit_employee_template.html",
                          {"form": form, "id": employee_id, "username": employee.admin.username})


def edit_role(request, role_id):
    role = Roles.objects.get(id=role_id)
    departments = Departments.objects.all()
    return render(request, "hod_template/edit_role_template.html",
                  {"role": role, "departments": departments, "id": role_id})


def edit_role_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        role_id = request.POST.get("role_id")
        role_name = request.POST.get("role_name")
        department_id = request.POST.get("department")

        try:
            role = Roles.objects.get(id=role_id)
            role.role_name = role_name
            department = Departments.objects.get(id=department_id)
            role.department_id = department
            role.save()

            messages.success(request, "Successfully Edited Role")
            return HttpResponseRedirect(reverse("edit_role", kwargs={"role_id": role_id}))
        except:
            messages.error(request, "Failed to Edit Role")
            return HttpResponseRedirect(reverse("edit_role", kwargs={"role_id": role_id}))


def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    return render(request, "hod_template/edit_department_template.html",
                  {"department": department, "id":department_id})

def edit_department_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        department_id = request.POST.get("course_id")
        department_name = request.POST.get("course")

        try:
            department = Departments.objects.get(id=department_id)
            department.course_name = department_name
            department.save()
            messages.success(request, "Successfully Edited Department")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": department_id}))
        except:
            messages.error(request, "Failed to Edit Department")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": department_id}))


def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


def add_session_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

