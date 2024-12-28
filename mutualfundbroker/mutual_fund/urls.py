from django.urls import path, include

urlpatterns = [path("api/v1/", include("mutual_fund.api.v1.urls"))]
