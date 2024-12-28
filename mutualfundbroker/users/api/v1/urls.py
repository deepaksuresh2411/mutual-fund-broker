from django.urls import re_path

from users.api.v1.views import (
    SignUpAPIView,
    SignInAPIView,
    SignOutAPIView,
    UserInvestmentDetailsAPIView,
)

urlpatterns = [
    re_path(r"^signup/$", SignUpAPIView.as_view(), name="signup"),
    re_path(r"^signin/$", SignInAPIView.as_view(), name="signin"),
    re_path(r"^signout/$", SignOutAPIView.as_view(), name="signout"),
    re_path(
        r"^investments/$",
        UserInvestmentDetailsAPIView.as_view(),
        name="user-investments",
    ),
]
