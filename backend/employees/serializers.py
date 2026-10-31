from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import AuditLog, Employee, EmployeeDocument, EmployeeHistory, LeaveRequest, PayPeriod, Payslip


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", required=False)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    department_name = serializers.CharField(source="department.name", read_only=True)
    class Meta:
        model = Employee
        fields = ["id", "employee_id", "username", "email", "first_name", "last_name", "phone", "position",
                  "hire_date", "salary", "department", "department_name", "is_active", "role", "status",
                  "termination_date", "termination_reason", "employment_type", "emergency_contact_name",
                  "emergency_contact_phone", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        for field in ("email", "first_name", "last_name"):
            if field in user_data:
                setattr(instance.user, field, user_data[field])
        instance.user.save()
        return super().update(instance, validated_data)


class EmployeeCreateSerializer(EmployeeSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, required=False, min_length=8)
    def create(self, validated_data):
        user_data = validated_data.pop("user", {})
        user_data["username"] = validated_data.pop("username")
        password = validated_data.pop("password", None) or get_random_string(length=12)
        user = User.objects.create_user(password=password, **user_data)
        return Employee.objects.create(user=user, **validated_data)


class EmployeeHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeHistory
        fields = "__all__"
        read_only_fields = ["changed_by", "created_at"]


class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source="employee.user.get_full_name", read_only=True)
    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ["status", "approver", "decision_at", "decision_notes", "created_at"]
        extra_kwargs = {"employee": {"required": False}}
    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError("End date must be on or after start date.")
        return attrs


class EmployeeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDocument
        fields = "__all__"
        read_only_fields = ["uploaded_by", "created_at"]


class PayPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPeriod
        fields = "__all__"
    def validate(self, attrs):
        if attrs["end_date"] < attrs["start_date"]:
            raise serializers.ValidationError("End date must be on or after start date.")
        return attrs


class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = "__all__"
        read_only_fields = ["net_pay", "created_at"]
    def validate(self, attrs):
        gross = attrs.get("gross_pay", self.instance.gross_pay if self.instance else 0)
        deductions = attrs.get("deductions", self.instance.deductions if self.instance else 0)
        attrs["net_pay"] = gross - deductions
        return attrs


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = "__all__"
        read_only_fields = ["actor", "created_at"]
