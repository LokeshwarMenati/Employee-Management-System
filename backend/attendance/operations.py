from django.utils import timezone
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AttendanceCorrection, Shift, Timesheet

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = "__all__"

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = "__all__"
        read_only_fields = ["approved_by"]

class AttendanceCorrectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceCorrection
        fields = "__all__"
        read_only_fields = ["requested_by", "status", "reviewed_by", "reviewed_at"]

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer

class TimesheetViewSet(viewsets.ModelViewSet):
    queryset = Timesheet.objects.select_related("employee", "shift")
    serializer_class = TimesheetSerializer
    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        obj = self.get_object()
        obj.status, obj.approved_by = "approved", request.user
        obj.save(update_fields=["status", "approved_by"])
        return Response(self.get_serializer(obj).data)

class AttendanceCorrectionViewSet(viewsets.ModelViewSet):
    queryset = AttendanceCorrection.objects.select_related("attendance", "requested_by")
    serializer_class = AttendanceCorrectionSerializer
    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user)
    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        obj = self.get_object()
        decision = request.data.get("status")
        if decision not in ("approved", "rejected"):
            return Response({"detail": "status must be approved or rejected"}, status=400)
        obj.status, obj.reviewed_by, obj.reviewed_at = decision, request.user, timezone.now()
        if decision == "approved":
            obj.attendance.check_in, obj.attendance.check_out = obj.requested_check_in, obj.requested_check_out
            obj.attendance.save(update_fields=["check_in", "check_out"])
        obj.save(update_fields=["status", "reviewed_by", "reviewed_at"])
        return Response(self.get_serializer(obj).data)
