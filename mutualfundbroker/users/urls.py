from django.urls import path, include

from users.views import DashboardView, AuthView

urlpatterns = [
    path("api/v1/", include("users.api.v1.urls")),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("auth/", AuthView.as_view(), name="auth"),
]
