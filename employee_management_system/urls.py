from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path

from django.urls import path
from employee_management_system import settings
from employee_management_app import views, HodViews, ManagerViews, EmployeeViews, EditResultViewClass
from employee_management_app.EditResultViewClass import EditResultViewClass

urlpatterns = [
    path('demo', views.showDemoPage),
    path('admin/', admin.site.urls),
    path('', views.ShowLoginPage, name="show_login"),
    path('doLogin', views.doLogin, name="do_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_manager', HodViews.add_manager, name="add_manager"),
    path('add_manager_save', HodViews.add_manager_save, name="add_manager_save"),
    path('add_department', HodViews.add_department, name="add_department"),
    path('add_department_save', HodViews.add_department_save, name="add_department_save"),
    path('add_employee', HodViews.add_employee, name="add_employee"),
    path('add_employee_save', HodViews.add_employee_save, name="add_employee_save"),
    path('manage_manager', HodViews.manage_manager, name="manage_manager"),
    path('manage_employee', HodViews.manage_employee, name="manage_employee"),
    path('manage_department', HodViews.manage_department, name="manage_department"),
    path('edit_manager/<str:manager_id>', HodViews.edit_manager, name="edit_manager"),
    path('edit_manager_save', HodViews.edit_manager_save, name="edit_manager_save"),
    path('edit_employee/<str:employee_id>', HodViews.edit_employee, name="edit_employee"),
    path('edit_employee_save', HodViews.edit_employee_save, name="edit_employee_save"),
    path('edit_department/<str:department_id>', HodViews.edit_department, name="edit_department"),
    path('edit_department_save', HodViews.edit_department_save, name="edit_department_save"),
    path('add_role', HodViews.add_role, name="add_role"),
    path('add_role_save', HodViews.add_role_save, name="add_role_save"),
    path('manage_role', HodViews.manage_role, name="manage_role"),
    path('edit_role/<str:role_id>', HodViews.edit_role, name="edit_role"),
    path('edit_role_save', HodViews.edit_role_save, name="edit_role_save"),
    path('manage_session', HodViews.manage_session, name="manage_session"),
    path('add_session_save', HodViews.add_session_save, name="add_session_save"),
    # manager Url Paths
    path('manager_home', ManagerViews.manager_home, name="manager_home"),
    path('manager_take_attendance', ManagerViews.manager_take_attendance, name="manager_take_attendance"),
    path('get_employees', ManagerViews.get_employees, name="get_employees"),
    path('save_attendance_data', ManagerViews.save_attendance_data, name="save_attendance_data"),
    path('manager_update_attendance', ManagerViews.manager_update_attendance, name="manager_update_attendance"),
    path('get_attendance_dates', ManagerViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_employee', ManagerViews.get_attendance_employee, name="get_attendance_employee"),
    path('save_updateattendance_data', ManagerViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('manager_add_result', ManagerViews.manager_add_result, name="manager_add_result"),
    path('save_employee_result', ManagerViews.save_employee_result, name="save_employee_result"),
    path('edit_employee_result', EditResultViewClass.as_view(), name="edit_employee_result"),
    path('fetch_result_employee', ManagerViews.fetch_result_employee, name="fetch_result_employee"),
    # employee Url Paths
    path('employee_home', EmployeeViews.employee_home, name="employee_home"),
    path('employee_view_attendance', EmployeeViews.employee_view_attendance, name="employee_view_attendance"),
    path('employee_view_attendance_post', EmployeeViews.employee_view_attendance_post,
         name="employee_view_attendance_post"),
    path('employee_view_result', EmployeeViews.employee_view_result, name="employee_view_result")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)
