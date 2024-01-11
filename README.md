# Employee Management System (EMS)

The Employee Management System (EMS) is a web-based application developed using the Django web framework in Python. It provides a comprehensive solution for managing employee data, attendance, appraisals, task assignments, and leave applications.

## Features

- **User Roles:**
  - Administrator: Manages employee data, system settings, and privileges.
  - Supervisor: Handles attendance, appraisals, task assignments for their team.
  - Subordinate Staff: Manages personal attendance, appraisals, and leave applications.

- **Functionality:**
  - Add, remove, and update employee information.
  - Attendance tracking with supervisor privileges.
  - Conduct appraisals and set goals for subordinates.
  - Assign tasks and view task assignments.
  - Apply for leave and view leave status.
  - Comprehensive analytics and reports for administrators.

## Getting Started

To run the Employee Management System locally, follow these steps:

### Prerequisites

1. Make sure you have Python3 and pip installed on your system.
2. Install MySQL database.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/employee-management-system.git
    ```

2. Navigate to the project directory:

    ```bash
    cd employee-management-system
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up MySQL database:
   - Create a database named `employee_management_system`.
   - Update database settings in `settings.py`:

      ```python
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.mysql',
              'NAME': 'employee_management_system',
              'USER': 'your_username',
              'PASSWORD': 'your_password',
              'HOST': 'localhost',
              'PORT': '3306',
          }
      }
      ```

5. Run migrations:

    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

### Running the Application

1. Start the Django development server:

    ```bash
    python3 manage.py runserver
    ```

2. Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the Employee Management System.

## Contributing

Feel free to contribute to the project by opening issues or submitting pull requests. Your feedback and collaboration are highly appreciated.


```