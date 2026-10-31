from django.core.exceptions import ValidationError
from django.db import models
from employees.models import Employee


class Attendance(models.Model):
    STATUS_CHOICES = [("present", "Present"), ("absent", "Absent"), ("late", "Late"), ("leave", "Leave")]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="attendance_records")
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="present")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "employee__employee_id"]
        constraints = [models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_attendance_date")]

    def clean(self):
        if self.check_in and self.check_out and self.check_out < self.check_in:
            raise ValidationError("Check-out time cannot be before check-in time.")

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date}"


class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)


class Timesheet(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="timesheets")
    date = models.DateField()
    shift = models.ForeignKey(Shift, null=True, blank=True, on_delete=models.SET_NULL)
    hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[("draft", "Draft"), ("submitted", "Submitted"), ("approved", "Approved")], default="draft")
    approved_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_timesheet_date")]


class AttendanceCorrection(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name="corrections")
    requested_by = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    requested_check_in = models.TimeField(null=True, blank=True)
    requested_check_out = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending")
    reviewed_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="reviewed_corrections")
    reviewed_at = models.DateTimeField(null=True, blank=True)
