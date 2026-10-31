from rest_framework.routers import DefaultRouter
from .views import AttendanceViewSet
from .operations import AttendanceCorrectionViewSet, ShiftViewSet, TimesheetViewSet

router = DefaultRouter()
router.register("attendance", AttendanceViewSet, basename="attendance")
router.register("shifts", ShiftViewSet, basename="shift")
router.register("timesheets", TimesheetViewSet, basename="timesheet")
router.register("attendance-corrections", AttendanceCorrectionViewSet, basename="attendance-correction")
urlpatterns = router.urls
