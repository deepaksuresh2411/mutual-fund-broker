from django.shortcuts import redirect
from django.urls import reverse


class AuthRedirectMiddleware:
    """
    Middleware to redirect users based on authentication status.
    - Redirects unauthenticated users to `/signin` if they're accessing other pages.
    - Redirects authenticated users away from `/signin` to `/dashboard`.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_path = request.path
        dashboard_path = reverse("dashboard")
        auth_path = reverse("auth")
        root_path = "/"

        if current_path == root_path:
            if request.user.is_authenticated:
                return redirect(dashboard_path)
            else:
                return redirect(auth_path)

        return self.get_response(request)
