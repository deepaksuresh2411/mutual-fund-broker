from rest_framework.response import Response


class UtilityMixin:
    def send_response(self, response: dict, status_code: int) -> Response:
        return Response(
            response,
            status=status_code,
        )
