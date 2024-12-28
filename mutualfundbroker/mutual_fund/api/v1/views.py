from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status, permissions, authentication

from mutual_fund.models import MutualFund, MutualFundFamily


class MutualFundFamilyAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        mf_houses = MutualFundFamily.objects.values_list("name", flat=True)
        return Response(
            {"mf_houses": mf_houses, "is_success": True}, status=status.HTTP_200_OK
        )


class MutualFundAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        fund_family = request.GET.get("fund_family")

        if fund_family:
            schemes = MutualFund.objects.filter(fund_family__name=fund_family).values(
                "scheme_name", "scheme_code", "net_asset_value"
            )
            return Response(
                {"schemes": schemes, "is_success": True}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Invalid Params", "is_success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
