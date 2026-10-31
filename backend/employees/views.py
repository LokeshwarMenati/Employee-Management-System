from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import BasePermission
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import AuditLog, Employee, EmployeeDocument, EmployeeHistory, LeaveRequest, PayPeriod, Payslip
from .serializers import (AuditLogSerializer, EmployeeCreateSerializer, EmployeeDocumentSerializer,
                          EmployeeHistorySerializer, EmployeeSerializer, LeaveRequestSerializer,
                          PayPeriodSerializer, PayslipSerializer)


class OperationsPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return bool(request.user and request.user.is_authenticated)
        profile = getattr(request.user, "employee_profile", None)
        if getattr(view, "basename", "") == "leave-request" and request.method == "POST":
            return bool(profile)
        return bool(request.user.is_staff or (profile and profile.role in {"admin", "hr", "manager", "finance"}))


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [OperationsPermission]
    allowed_roles = {"admin", "hr", "manager", "finance"}
    def perform_create(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(actor=self.request.user, action="create", model_name=obj.__class__.__name__, object_id=obj.pk)
    def perform_update(self, serializer):
        obj = serializer.save()
        AuditLog.objects.create(actor=self.request.user, action="update", model_name=obj.__class__.__name__, object_id=obj.pk)


class EmployeeViewSet(viewsets.ModelViewSet):
    permission_classes = [OperationsPermission]
    queryset = Employee.objects.select_related("user", "department").all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["employee_id", "user__username", "user__first_name", "user__last_name", "position"]
    ordering_fields = ["employee_id", "hire_date", "created_at"]
    ordering = ["employee_id"]

    def get_serializer_class(self):
        return EmployeeCreateSerializer if self.action == "create" else EmployeeSerializer


class EmployeeHistoryViewSet(RoleViewSet):
    queryset = EmployeeHistory.objects.select_related("employee", "changed_by")
    serializer_class = EmployeeHistorySerializer
    def perform_create(self, serializer):
        serializer.save(changed_by=self.request.user)


class LeaveRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [OperationsPermission]
    queryset = LeaveRequest.objects.select_related("employee__user", "approver")
    serializer_class = LeaveRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["employee", "status", "leave_type"]
    def get_queryset(self):
        qs = super().get_queryset()
        profile = getattr(self.request.user, "employee_profile", None)
        if profile and profile.role == "employee":
            return qs.filter(employee=profile)
        return qs
    def perform_create(self, serializer):
        profile = getattr(self.request.user, "employee_profile", None)
        employee = profile if profile and profile.role == "employee" else serializer.validated_data.get("employee") or profile
        serializer.save(employee=employee)
    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        return self._decide(request, "approved")
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        return self._decide(request, "rejected")
    def _decide(self, request, decision):
        leave = self.get_object()
        leave.status, leave.approver, leave.decision_at = decision, request.user, timezone.now()
        leave.decision_notes = request.data.get("decision_notes", "")
        leave.save(update_fields=["status", "approver", "decision_at", "decision_notes"])
        AuditLog.objects.create(actor=request.user, action=decision, model_name="LeaveRequest", object_id=leave.pk)
        return Response(self.get_serializer(leave).data)


class EmployeeDocumentViewSet(RoleViewSet):
    queryset = EmployeeDocument.objects.select_related("employee", "uploaded_by")
    serializer_class = EmployeeDocumentSerializer
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class PayPeriodViewSet(RoleViewSet):
    queryset = PayPeriod.objects.all()
    serializer_class = PayPeriodSerializer


class PayslipViewSet(RoleViewSet):
    queryset = Payslip.objects.select_related("employee", "pay_period")
    serializer_class = PayslipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["employee", "pay_period", "status"]


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("actor")
    serializer_class = AuditLogSerializer
