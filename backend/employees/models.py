from django.contrib.auth.models import User
from django.db import models


class Employee(models.Model):
    ROLE_CHOICES = [("admin", "Admin"), ("hr", "HR"), ("manager", "Manager"), ("employee", "Employee"), ("finance", "Finance")]
    STATUS_CHOICES = [("active", "Active"), ("onboarding", "Onboarding"), ("on_leave", "On leave"), ("terminated", "Terminated"), ("inactive", "Inactive")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee_profile")
    employee_id = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, blank=True)
    position = models.CharField(max_length=100, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    department = models.ForeignKey("departments.Department", null=True, blank=True, on_delete=models.SET_NULL, related_name="employees")
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.TextField(blank=True)
    employment_type = models.CharField(max_length=30, default="full_time")
    emergency_contact_name = models.CharField(max_length=150, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"


class EmployeeHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="lifecycle_history")
    event_type = models.CharField(max_length=40)
    effective_date = models.DateField()
    notes = models.TextField(blank=True)
    changed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-effective_date", "-id"]


class LeaveRequest(models.Model):
    TYPES = [("annual", "Annual"), ("sick", "Sick"), ("unpaid", "Unpaid"), ("other", "Other")]
    STATUSES = [("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected"), ("cancelled", "Cancelled")]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leave_requests")
    leave_type = models.CharField(max_length=20, choices=TYPES, default="annual")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="pending")
    approver = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_leave_requests")
    decision_at = models.DateTimeField(null=True, blank=True)
    decision_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


class EmployeeDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=60)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="employee_documents/%Y/%m/")
    issued_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class PayPeriod(models.Model):
    STATUSES = [("open", "Open"), ("processing", "Processing"), ("closed", "Closed")]
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    pay_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="open")

    class Meta:
        ordering = ["-start_date"]
        constraints = [models.UniqueConstraint(fields=["start_date", "end_date"], name="unique_pay_period")]


class Payslip(models.Model):
    STATUSES = [("draft", "Draft"), ("approved", "Approved"), ("paid", "Paid")]
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE, related_name="payslips")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="payslips")
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_pay = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default="draft")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["pay_period", "employee"], name="unique_period_employee_payslip")]


class AuditLog(models.Model):
    actor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=30)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=64, blank=True)
    details = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
