from rest_framework.routers import DefaultRouter
from .views import (AuditLogViewSet, EmployeeDocumentViewSet, EmployeeHistoryViewSet,
                    EmployeeViewSet, LeaveRequestViewSet, PayPeriodViewSet, PayslipViewSet)

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")
router.register("employee-history", EmployeeHistoryViewSet, basename="employee-history")
router.register("leave-requests", LeaveRequestViewSet, basename="leave-request")
router.register("employee-documents", EmployeeDocumentViewSet, basename="employee-document")
router.register("pay-periods", PayPeriodViewSet, basename="pay-period")
router.register("payslips", PayslipViewSet, basename="payslip")
router.register("audit-logs", AuditLogViewSet, basename="audit-log")
urlpatterns = router.urls
