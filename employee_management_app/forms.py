from django import forms
from django.forms import ChoiceField

from employee_management_app.models import Departments, SessionYearModel, Roles, Employees

class ChoiceNoValidation(ChoiceField):
    def validate(self, value):
        pass

class DateInput(forms.DateInput):
    input_type = "date"

class AddEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control", "autocomplete": "off"}))
    password = forms.CharField(label="Password", max_length=50, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    department_list = []

    try:
        departments = Departments.objects.all()
        for department in departments:
            small_department = (department.id, department.department_name)
            department_list.append(small_department)
    except:
        department_list = []

    session_list = []

    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year) + " TO " + str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list = []

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    department = forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", max_length=50, widget=forms.FileInput(attrs={"class": "form-control"}))

class EditEmployeeForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))

    department_list = []

    try:
        departments = Departments.objects.all()
        for department in departments:
            small_department = (department.id, department.department_name)
            department_list.append(small_department)
    except:
        department_list = []

    session_list = []

    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year) + " TO " + str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list = []

    gender_choice = (
        ("Male", "Male"),
        ("Female", "Female")
    )

    department = forms.ChoiceField(label="Department", choices=department_list, widget=forms.Select(attrs={"class": "form-control"}))
    sex = forms.ChoiceField(label="Sex", choices=gender_choice, widget=forms.Select(attrs={"class": "form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", max_length=50, widget=forms.FileInput(attrs={"class": "form-control"}), required=False)

class EditResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.employee_id = kwargs.pop("employee_id")
        super(EditResultForm, self).__init__(*args, **kwargs)
        role_list = []
        try:
            roles = Roles.objects.filter(employee_id=self.employee_id)
            for role in roles:
                role_single = (role.id, role.role_name)
                role_list.append(role_single)
        except:
            role_list = []
        self.fields['role_id'].choices = role_list

    session_list = []
    try:
        sessions = SessionYearModel.object.all()
        for session in sessions:
            session_single = (session.id, str(session.session_start_year) + " TO " + str(session.session_end_year))
            session_list.append(session_single)
    except:
        session_list = []

    role_id = forms.ChoiceField(label="Role", widget=forms.Select(attrs={"class": "form-control"}))
    session_ids = forms.ChoiceField(label="Session Year", choices=session_list, widget=forms.Select(attrs={"class": "form-control"}))
    employee_ids = ChoiceNoValidation(label="Employee", widget=forms.Select(attrs={"class": "form-control"}))
    assignment_marks = forms.CharField(label="Mid Year Marks", widget=forms.TextInput(attrs={"class": "form-control"}))
    exam_marks = forms.CharField(label="End of year Marks", widget=forms.TextInput(attrs={"class": "form-control"}))
