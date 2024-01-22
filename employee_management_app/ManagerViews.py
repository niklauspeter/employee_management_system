import json
from django.shortcuts import render

from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from employee_management_app.models import Roles, SessionYearModel, Employees, Attendance, AttendanceReport, \
    LeaveReportEmployees, Managers, FeedBackManagers, CustomUser, Departments, NotificationManagers, EmployeeResult, OnlineClassRoom

def manager_home(request):
    # For Fetch All Employee Under Manager
    roles = Roles.objects.filter(manager_id=request.user.id)
    department_id_list = []
    for role in roles:
        department = Departments.objects.get(id=role.department_id.id)
        department_id_list.append(department.id)

    final_department = []
    # removing Duplicate Department ID
    for department_id in department_id_list:
        if department_id not in final_department:
            final_department.append(department_id)

    employees_count = Employees.objects.filter(department_id__in=final_department).count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(role_id__in=roles).count()

    # Fetch All Approve Leave
    manager = Managers.objects.get(admin=request.user.id)
    leave_count = LeaveReportEmployees.objects.filter(manager_id=manager.id, leave_status=1).count()
    role_count = roles.count()

    # Fetch Attendance Data by Role
    role_list = []
    attendance_list = []
    for role in roles:
        attendance_count1 = Attendance.objects.filter(role_id=role.id).count()
        role_list.append(role.role_name)
        attendance_list.append(attendance_count1)

    employees_attendance = Employees.objects.filter(department_id__in=final_department)
    employee_list = []
    employee_list_attendance_present = []
    employee_list_attendance_absent = []
    for employee in employees_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, employee_id=employee.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, employee_id=employee.id).count()
        employee_list.append(employee.admin.username)
        employee_list_attendance_present.append(attendance_present_count)
        employee_list_attendance_absent.append(attendance_absent_count)

    return render(request, "manager_template/manager_home_template.html",
                  {"employees_count": employees_count, "attendance_count": attendance_count,
                   "leave_count": leave_count, "role_count": role_count, "role_list": role_list,
                   "attendance_list": attendance_list, "employee_list": employee_list,
                   "present_list": employee_list_attendance_present,
                   "absent_list": employee_list_attendance_absent})


def manager_take_attendance(request):
    roles = Roles.objects.filter(manager_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "manager_template/manager_take_attendance.html", {"roles": roles, "session_years": session_years})

@csrf_exempt
def get_employees(request):
    role_id = request.POST.get("role")
    session_year = request.POST.get("session_year")

    role = Roles.objects.get(id=role_id)
    session_model = SessionYearModel.object.get(id=session_year)
    employees = Employees.objects.filter(department_id=role.department_id, session_year_id=session_model)
    list_data = []

    for employee in employees:
        data_small = {"id": employee.admin.id, "name": employee.admin.first_name + " " + employee.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_attendance_data(request):
    employee_ids = request.POST.get("employee_ids")
    role_id = request.POST.get("role_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    role_model = Roles.objects.get(id=role_id)
    session_model = SessionYearModel.object.get(id=session_year_id)
    json_employees = json.loads(employee_ids)

    try:
        attendance = Attendance(role_id=role_model, attendance_date=attendance_date, session_year_id=session_model)
        attendance.save()

        for emp in json_employees:
            employee = Employees.objects.get(admin=emp['id'])
            attendance_report = AttendanceReport(employee_id=employee, attendance_id=attendance, status=emp['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def manager_update_attendance(request):
    roles = Roles.objects.filter(manager_id=request.user.id)
    session_year_id = SessionYearModel.object.all()
    return render(request, "manager_template/manager_update_attendance.html", {"roles": roles, "session_year_id": session_year_id})

@csrf_exempt
def get_attendance_dates(request):
    role = request.POST.get("role")
    session_year_id = request.POST.get("session_year_id")
    role_obj = Roles.objects.get(id=role)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(role_id=role_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)

@csrf_exempt
def get_attendance_employee(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for employee in attendance_data:
        data_small = {"id": employee.employee_id.admin.id,
                      "name": employee.employee_id.admin.first_name + " " + employee.employee_id.admin.last_name,
                      "status": employee.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)

@csrf_exempt
def save_update_attendance_data(request):
    employee_ids = request.POST.get("employee_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_employees = json.loads(employee_ids)

    try:
        for emp in json_employees:
            employee = Employees.objects.get(admin=emp['id'])
            attendance_report = AttendanceReport.objects.get(employee_id=employee, attendance_id=attendance)
            attendance_report.status = emp['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def manager_add_result(request):
    roles = Roles.objects.filter(manager_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "manager_template/manager_add_result.html", {"roles": roles, "session_years": session_years})

def save_employee_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect('manager_add_result')
    employee_admin_id = request.POST.get('employee_list')
    assignment_marks = request.POST.get('assignment_marks')
    exam_marks = request.POST.get('exam_marks')
    role_id = request.POST.get('role')

    employee_obj = Employees.objects.get(admin=employee_admin_id)
    role_obj = Roles.objects.get(id=role_id)

    try:
        check_exist = EmployeeResult.objects.filter(role_id=role_obj, employee_id=employee_obj).exists()
        if check_exist:
            result = EmployeeResult.objects.get(role_id=role_obj, employee_id=employee_obj)
            result.assignment_marks = assignment_marks
            result.exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("manager_add_result"))
        else:
            result = EmployeeResult(employee_id=employee_obj, role_id=role_obj, exam_marks=exam_marks,
                                    assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("manager_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("manager_add_result"))

@csrf_exempt
def fetch_result_employee(request):
    role_id = request.POST.get('role_id')
    employee_id = request.POST.get('employee_id')
    employee_obj = Employees.objects.get(admin=employee_id)
    result = EmployeeResult.objects.filter(employee_id=employee_obj.id, role_id=role_id).exists()
    if result:
        result = EmployeeResult.objects.get(employee_id=employee_obj.id, role_id=role_id)
        result_data = {"exam_marks": result.exam_marks, "assignment_marks": result.assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")