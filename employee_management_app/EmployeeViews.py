from django.shortcuts import render
import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from employee_management_app.models import Employees, Departments, Roles, CustomUser, Attendance, AttendanceReport, LeaveReportEmployee, EmployeeResult, SessionYearModel


def employee_home(request):
    employee_final_result = []
    employee_mid_result = []

    employee_obj = Employees.objects.get(admin=request.user.id)
    employeeresult = EmployeeResult.objects.filter(employee_id=employee_obj.id)
    attendance_total = AttendanceReport.objects.filter(employee_id=employee_obj).count()
    attendance_present = AttendanceReport.objects.filter(employee_id=employee_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(employee_id=employee_obj, status=False).count()
    department = Departments.objects.get(id=employee_obj.department_id.id)
    roles = Roles.objects.filter(department_id=department).count()
    roles_data = Roles.objects.filter(department_id=department)
    session_obj = SessionYearModel.object.get(id=employee_obj.session_year_id.id)
    class_room = OnlineClassRoom.objects.filter(role__in=roles_data, is_active=True, session_years=session_obj)

    for employee_result in employeeresult:
        employee_final_result.append(int(employee_result.exam_marks))
        employee_mid_result.append(int(employee_result.assignment_marks))

    role_name = []
    data_present = []
    data_absent = []
    role_data = Roles.objects.filter(department_id=employee_obj.department_id)
    for role in role_data:
        attendance = Attendance.objects.filter(role_id=role.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   employee_id=employee_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,
                                                                  employee_id=employee_obj.id).count()
        role_name.append(role.role_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    return render(request, "employee_template/employee_home_template.html",
                  {"total_attendance": attendance_total, "attendance_absent": attendance_absent,
                   "attendance_present": attendance_present, "roles": roles, "data_name": role_name,
                   "data1": data_present, "data2": data_absent, "class_room": class_room,
                   "data3": employee_mid_result, "data4": employee_final_result})


def employee_view_attendance(request):
    employee = Employees.objects.get(admin=request.user.id)
    department = employee.department_id
    roles = Roles.objects.filter(department_id=department)
    return render(request, "employee_template/employee_view_attendance.html", {"roles": roles})


def employee_view_attendance_post(request):
    role_id = request.POST.get("role")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    role_obj = Roles.objects.get(id=role_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    emp_obj = Employees.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                           role_id=role_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, employee_id=emp_obj)
    return render(request, "employee_template/employee_attendance_data.html",
                  {"attendance_reports": attendance_reports})


def employee_view_result(request):
    employee = Employees.objects.get(admin=request.user.id)
    employeeresult = EmployeeResult.objects.filter(employee_id=employee.id)
    return render(request, "employee_template/employee_result.html", {"employeeresult": employeeresult})
