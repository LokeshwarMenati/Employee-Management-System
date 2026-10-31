from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(read_only=True)
    manager_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "description", "manager", "manager_name", "employee_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_manager_name(self, obj):
        return obj.manager.user.get_full_name() if obj.manager else None
