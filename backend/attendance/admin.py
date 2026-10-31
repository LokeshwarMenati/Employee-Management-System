from django.contrib import admin
from .models import Attendance, AttendanceCorrection, Shift, Timesheet

for model in (Attendance, Shift, Timesheet, AttendanceCorrection):
    admin.site.register(model)
