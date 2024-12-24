from django.urls import re_path

from users.api.v1.views import SignUpAPIView, SignInAPIView, SignOutAPIView

urlpatterns = [
    re_path(r"^signup/$", SignUpAPIView.as_view(), name="signup"),
    re_path(r"^signin/$", SignInAPIView.as_view(), name="signin"),
    re_path(r"^signout/$", SignOutAPIView.as_view(), name="signout"),
]
