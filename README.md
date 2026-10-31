# Employee Management System — Full-Stack Administration System

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2+-092E20?style=flat&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.18+-a30000?style=flat&logo=django&logoColor=white)
![Angular](https://img.shields.io/badge/Angular-17-DD0031?style=flat&logo=angular&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6?style=flat&logo=typescript&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Ready-4479A1?style=flat&logo=mysql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Dev-003B57?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-4c1?style=flat)

A full-stack employee administration system built with Angular, Django REST Framework, and MySQL.

## Project layout

```text
Employee Management System/
├── backend/                 # Django REST API
│   ├── config/              # Settings, root URLs, WSGI/ASGI
│   ├── authentication/      # Login, logout, profile, password APIs
│   ├── employees/           # Employee model and CRUD API
│   ├── departments/         # Department model and CRUD API
│   ├── attendance/          # Attendance model and CRUD API
│   └── dashboard/           # Aggregated dashboard API
└── frontend/employee-app/   # Angular single-page application
    └── src/app/             # Pages, services, guards, models, and shared UI
```

## Backend setup

1. Create and activate a virtual environment:

   ```powershell
   cd "Employee Management System\backend"
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and set the MySQL values. SQLite is used when
   `DB_ENGINE` is omitted, which makes local API development possible without
   MySQL.

3. Apply migrations and create an administrator:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

The API is available at `http://localhost:8000/api/` and the Django admin is
available at `http://localhost:8000/admin/`.

## Frontend setup

```powershell
cd "Employee Management System\frontend\employee-app"
npm install
npm start
```

The Angular application is available at `http://localhost:4200/`. Its
development environment points to `http://localhost:8000/api`.

The dashboard includes a dark-premium executive view with attendance trends,
department distribution, KPI cards, and recent activity. The local SQLite
database in this workspace contains demo records for six employees, four
departments, and attendance history so the screens can be explored immediately.

## Demo walkthrough

For local exploration, sign in with:

- Username: `user`
- Password: `user`

Use the sidebar in this order:

1. **People** — inspect six employees, roles, departments, employment status,
   and lifecycle history.
2. **Leave approvals** — review four requests containing pending, approved, and
   rejected examples.
3. **Shifts & timesheets** — compare three shifts and six timesheets with
   submitted and approved states.
4. **Payroll** — inspect the October 2026 pay period and six payslips with
   gross pay, deductions, net pay, and payment status.
5. **Documents** — inspect identity and contract records, including expiry
   dates and upload metadata.
6. **Reports & export** — download operational CSV output.
7. **Audit log** — review sample create, approve, upload, and process events.

The demo data is safe to recreate and is intended only for local learning. It
does not represent real employees or production payroll data.

## API overview

| Area | Endpoints |
| --- | --- |
| Authentication | `POST /api/login/`, `POST /api/logout/`, `GET/PATCH /api/profile/`, `POST /api/profile/change-password/` |
| Employees | `GET/POST /api/employees/`, `GET/PUT/DELETE /api/employees/{id}/`, `/api/employee-history/` |
| Departments | `GET/POST /api/departments/`, `GET/PUT/DELETE /api/departments/{id}/` |
| Attendance | `GET/POST /api/attendance/`, `/api/shifts/`, `/api/timesheets/`, `/api/attendance-corrections/` |
| HR operations | `/api/leave-requests/`, `/api/employee-documents/`, `/api/pay-periods/`, `/api/payslips/`, `/api/audit-logs/` |
| Dashboard | `GET /api/dashboard/` |
| Reporting | `GET /api/reports/export/` |

All protected endpoints use token authentication:

```text
Authorization: Token <token>
```

## Postman smoke test

1. `POST http://localhost:8000/api/login/` with
   `{"username":"<admin>","password":"<password>"}`.
2. Save the returned token as a Postman environment variable.
3. Add `Authorization: Token {{token}}` to protected requests.
4. Create a department, create an employee using its department ID, and post
   attendance for that employee.
5. Request `/api/dashboard/` to verify the aggregate metrics.

## Production notes

- Set `DEBUG=False`, a strong `SECRET_KEY`, explicit `ALLOWED_HOSTS`, and
  `CORS_ALLOWED_ORIGINS` in the backend environment.
- Use MySQL by setting `DB_ENGINE=mysql` and the database connection variables
  in `.env`.
- Build the Angular app with `npm run build` and serve the generated `dist`
  directory behind a web server or CDN.
