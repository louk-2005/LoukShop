#rest_frame files
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if not response:
        return Response(
            data={'message':f'server error{exc}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            exception=True
        )
    return Response(
        data={'message':f'server error{exc}'},
        status=response.status_code,
        exception=True
    )








