from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from employee_management_app.forms import EditResultForm
from employee_management_app.models import Employees, Roles, EmployeeResult


class EditResultViewClass(View):
    def get(self, request, *args, **kwargs):
        manager_id = request.user.id
        edit_result_form = EditResultForm(manager_id=manager_id)
        return render(request, "manager_template/edit_employee_result.html", {"form": edit_result_form})

    def post(self, request, *args, **kwargs):
        form = EditResultForm(manager_id=request.user.id, data=request.POST)
        if form.is_valid():
            employee_admin_id = form.cleaned_data['employee_ids']
            assignment_marks = form.cleaned_data['assignment_marks']
            exam_marks = form.cleaned_data['exam_marks']
            role_id = form.cleaned_data['role_id']

            employee_obj = Employees.objects.get(admin=employee_admin_id)
            role_obj = Roles.objects.get(id=role_id)
            result = EmployeeResult.objects.get(role_id=role_obj, employee_id=employee_obj)
            result.assignment_marks = assignment_marks
            result.exam_marks = exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("edit_employee_result"))
        else:
            messages.error(request, "Failed to Update Result")
            form = EditResultForm(request.POST, manager_id=request.user.id)
            return render(request, "manager_template/edit_employee_result.html", {"form": form})
