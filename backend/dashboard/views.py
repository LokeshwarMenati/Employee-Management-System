from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
import csv
from attendance.models import Attendance
from departments.models import Department
from employees.models import Employee
from attendance.serializers import AttendanceSerializer


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        records = Attendance.objects.filter(date=today)
        recent = Attendance.objects.select_related("employee__user").order_by("-date", "-id")[:8]
        weekly = []
        for offset in range(6, -1, -1):
            date = today - timedelta(days=offset)
            day_records = Attendance.objects.filter(date=date)
            weekly.append({
                "date": date.isoformat(),
                "present": day_records.filter(status="present").count(),
                "late": day_records.filter(status="late").count(),
                "absent": day_records.filter(status="absent").count(),
                "leave": day_records.filter(status="leave").count(),
            })
        return Response({
            "total_employees": Employee.objects.filter(is_active=True).count(),
            "active_employees": Employee.objects.filter(is_active=True).count(),
            "total_departments": Department.objects.count(),
            "present_today": records.filter(status="present").count(),
            "late_today": records.filter(status="late").count(),
            "absent_today": records.filter(status="absent").count(),
            "leave_today": records.filter(status="leave").count(),
            "attendance_rate": round(
                records.filter(status__in=["present", "late"]).count()
                / records.count() * 100, 1
            ) if records.exists() else 0,
            "department_breakdown": list(Department.objects.annotate(employee_count=Count("employees")).values("id", "name", "employee_count")),
            "weekly_attendance": weekly,
            "recent_attendance": AttendanceSerializer(recent, many=True).data,
        })


class ReportExportView(APIView):
    """Export a compact employee/attendance report for finance and HR."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="hr-report.csv"'
        writer = csv.writer(response)
        writer.writerow(["employee_id", "employee", "department", "status", "attendance_days"])
        for employee in Employee.objects.select_related("user", "department").all():
            writer.writerow([employee.employee_id, employee.user.get_full_name() or employee.user.username,
                             employee.department.name if employee.department else "", employee.status,
                             employee.attendance_records.count()])
        return response
