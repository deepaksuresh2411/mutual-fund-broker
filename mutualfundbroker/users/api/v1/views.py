from datetime import datetime

from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import APIView, GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
from rest_framework import permissions, authentication
from django.contrib.auth.password_validation import validate_password

from users.models import Appuser, UserInvestDetails
from users.api.v1.mixins import UtilityMixin


class AuthView(GenericAPIView, UtilityMixin):
    permission_classes = [permissions.AllowAny]


class SignUpAPIView(AuthView):

    def post(self, request, *args, **kwargs):

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        password = request.data.get("password1")

        if Appuser.objects.filter(email__iexact=email).exists():
            return self.send_response(
                {
                    "message": "User with this email id already exists!",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            validate_password(password=password)
        except ValidationError as e:
            return self.send_response(
                {"message": e.messages, "is_success": False},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user = Appuser.objects.create_user(
            email=email, password=password, first_name=first_name, last_name=last_name
        )
        token, _ = Token.objects.get_or_create(user=user)
        return self.send_response(
            {
                "message": "Signed up successfully",
                "token": token.key if token else "",
                "is_success": True,
            },
            status_code=status.HTTP_201_CREATED,
        )


class SignInAPIView(AuthView):

    def post(self, request, *args, **kwargs):
        email, password = request.data.get("email"), request.data.get("password")
        user = authenticate(request=request, email=email, password=password)
        if not user:
            return self.send_response(
                {"message": "Invalid Username or Password", "is_success": False},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)

        return self.send_response(
            {
                "message": "Signed In successfully",
                "token": token.key if token else "",
                "is_success": True,
            },
            status_code=status.HTTP_200_OK,
        )


class SignOutAPIView(AuthView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Token "):
            return self.send_response(
                {
                    "message": "Invalid or missing Authorization header",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token_key = auth_header.split(" ")[1]
            token = Token.objects.get(key=token_key)
            token.delete()
            return self.send_response(
                {"message": "Logged out successfully", "is_success": True},
                status_code=status.HTTP_200_OK,
            )
        except Token.DoesNotExist:
            return self.send_response(
                {
                    "message": "Invalid token",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )


class UserInvestmentDetailsAPIView(APIView, UtilityMixin):

    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        data = request.data
        partial_data_error_message = ""

        if not "schema_code" in data:
            partial_data_error_message += "schema_code is required, "

        if not "invested_date" in data:
            partial_data_error_message += "invested_date is required, "

        if not "units_owned" in data:
            partial_data_error_message += "units_owned is required"

        if partial_data_error_message:
            return self.send_response(
                {"message": partial_data_error_message, "is_success": False},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        invested_date = None
        try:
            invested_date = datetime.strptime(data.get("invested_date"), "%d-%m-%Y")
        except Exception as e:
            return self.send_response(
                {
                    "message": "invested_date format error (required format is dd/mm/YYYY)",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        units_owned = 0
        try:
            units_owned = int(data.get("units_owned"))
        except Exception as e:
            return self.send_response(
                {
                    "message": "incorrect value in units_owned",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        UserInvestDetails.objects.create(
            user=request.user,
            mutual_fund=data.get("schema_code"),
            units_owned=units_owned,
            investment_date=invested_date,
        )
        
        
