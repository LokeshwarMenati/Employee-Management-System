from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)
    employee_id = serializers.CharField(source="employee.employee_id", read_only=True)

    class Meta:
        model = Attendance
        fields = ["id", "employee", "employee_id", "employee_name", "date", "check_in", "check_out", "status", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        if attrs.get("check_in") and attrs.get("check_out") and attrs["check_out"] < attrs["check_in"]:
            raise serializers.ValidationError("Check-out time cannot be before check-in time.")
        return attrs
