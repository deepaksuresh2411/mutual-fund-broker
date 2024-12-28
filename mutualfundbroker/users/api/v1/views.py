from datetime import datetime

from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ValidationError
from rest_framework import permissions, authentication
from rest_framework.generics import GenericAPIView
from django.contrib.auth.password_validation import validate_password

from users.api.v1.mixins import UtilityMixin
from mutual_fund.models import MutualFund
from users.models import Appuser, UserInvestDetails
from users.api.v1.serializers import UserInvestmentsModelSerializer


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
                {"message": "Signed out successfully", "is_success": True},
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
        investments = UserInvestDetails.objects.filter(user=request.user)
        serializer = UserInvestmentsModelSerializer(investments, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        partial_data_error_message = ""

        if not "scheme_code" in data:
            partial_data_error_message += "scheme_code is required, "

        if not "invested_date" in data:
            partial_data_error_message += "invested_date is required, "

        if not "units_owned" in data:
            partial_data_error_message += "units_owned is required, "

        if not "invested_amount" in data:
            partial_data_error_message += "invested_amount is required"

        if partial_data_error_message:
            return self.send_response(
                {"message": partial_data_error_message, "is_success": False},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        invested_date = None
        try:
            invested_date = datetime.strptime(data.get("invested_date"), "%Y-%m-%d")
        except Exception as e:
            return self.send_response(
                {
                    "message": "invested_date format error (required format is YYYY-MM-DD)",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        mutual_fund_obj = MutualFund.objects.filter(
            scheme_code__iexact=data.get("scheme_code", "")
        ).last()

        if not mutual_fund_obj:
            return self.send_response(
                {
                    "message": "Schema Code is not found",
                    "is_success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        curr_user_investment = UserInvestDetails.objects.filter(
            user=request.user, mutual_fund=mutual_fund_obj
        ).last()

        if curr_user_investment:
            curr_user_investment.units_owned = (
                curr_user_investment.units_owned + data.get("units_owned")
            )
            curr_user_investment.amount_invested = (
                curr_user_investment.amount_invested + data.get("invested_amount")
            )
            curr_user_investment.investment_date = invested_date
            curr_user_investment.save()
        else:
            UserInvestDetails.objects.create(
                user=request.user,
                mutual_fund=mutual_fund_obj,
                units_owned=data.get("units_owned", 0),
                investment_date=invested_date,
                amount_invested=data.get("invested_amount", 0),
            )
        return Response(
            {"message": "successfully created", "is_success": True},
            status=status.HTTP_201_CREATED,
        )

    def put(self, request, *args, **kwargs):
        investment_record_id = request.GET.get("investment")
        investment = UserInvestDetails.objects.filter(
            user=request.user, id=investment_record_id
        ).last()
        data = request.data
        if investment:
            is_updated = False
            if data.get("units_owned"):
                investment.units_owned = data.get("units_owned")
                is_updated = True
            if data.get("invested_amount"):
                investment.amount_invested = data.get("invested_amount")
                is_updated = True
            if data.get("invested_date"):
                invested_date = None
                try:
                    invested_date = datetime.strptime(
                        data.get("invested_date"), "%Y-%m-%d"
                    )
                    is_updated = True
                except Exception as e:
                    return self.send_response(
                        {
                            "message": "invested_date format error (required format is YYYY-MM-DD)",
                            "is_success": False,
                        },
                        status_code=status.HTTP_400_BAD_REQUEST,
                    )
                investment.investment_date = invested_date
            if is_updated:
                investment.save()
        else:
            return Response(
                {
                    "message": f"Investment ({investment_record_id}) is not found",
                    "is_success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "message": f"Investment ({investment_record_id}) is updated successfully",
                "is_success": True,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, *args, **kwargs):
        investment_record_id = request.GET.get("investment")
        investment = UserInvestDetails.objects.filter(
            user=request.user, id=investment_record_id
        ).last()

        if investment:
            investment.delete()
        else:
            return Response(
                {
                    "message": f"Investment ({investment_record_id}) is not found",
                    "is_success": False,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {
                "message": f"Investment ({investment_record_id}) is deleted successfully",
                "is_success": True,
            },
            status=status.HTTP_200_OK,
        )
