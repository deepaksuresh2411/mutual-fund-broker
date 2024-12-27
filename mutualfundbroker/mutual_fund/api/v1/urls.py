from django.urls import path

from mutual_fund.api.v1.views import MutualFundAPIView, MutualFundFamilyAPIView

urlpatterns = [
    path("fund-families/", MutualFundFamilyAPIView.as_view(), name="fund-family"),
    path("fund-schemes/", MutualFundAPIView.as_view(), name="fund-schemes"),
]
