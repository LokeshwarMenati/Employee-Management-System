from django.contrib import admin
from .models import AuditLog, Employee, EmployeeDocument, EmployeeHistory, LeaveRequest, PayPeriod, Payslip

for model in (Employee, EmployeeHistory, LeaveRequest, EmployeeDocument, PayPeriod, Payslip, AuditLog):
    admin.site.register(model)
