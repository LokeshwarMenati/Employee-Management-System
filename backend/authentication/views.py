from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


def user_payload(user):
    payload = {"id": user.id, "username": user.username, "email": user.email,
               "first_name": user.first_name, "last_name": user.last_name}
    profile = getattr(user, "employee_profile", None)
    if profile:
        payload.update({"role": profile.role, "employee_id": profile.employee_id, "status": profile.status})
    return payload


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get("username") or request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=username, password=password) if username and password else None
        if not user:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user_payload(user)})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.auth:
            request.auth.delete()
        return Response({"detail": "Logged out successfully."})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(user_payload(request.user))
    def patch(self, request):
        for field in ("email", "first_name", "last_name"):
            if field in request.data:
                setattr(request.user, field, request.data[field])
        request.user.save(update_fields=["email", "first_name", "last_name"])
        return Response(user_payload(request.user))


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        old_password, new_password = request.data.get("old_password"), request.data.get("new_password")
        if not old_password or not new_password or not request.user.check_password(old_password):
            return Response({"detail": "Current password is incorrect."}, status=400)
        if len(new_password) < 8:
            return Response({"detail": "New password must be at least 8 characters."}, status=400)
        request.user.set_password(new_password)
        request.user.save(update_fields=["password"])
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Password changed successfully.", "token": Token.objects.create(user=request.user).key})
