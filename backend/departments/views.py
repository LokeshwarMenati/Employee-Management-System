from django.db.models import Count
from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.annotate(employee_count=Count("employees")).select_related("manager__user")
    serializer_class = DepartmentSerializer
