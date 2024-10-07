"""Middleware связанные с работой Pydantic."""
import logging

from django.http import JsonResponse
from rest_framework import status

from server.errors.http_errors import HTTP_ERRORS
from pydantic.error_wrappers import ValidationError

logger = logging.getLogger(__name__)


class PydanticDeserializeJsonMiddleware:
    """Middleware отлова и обработки ошибок валидации библиотеки Pydantic."""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, ValidationError):
            logger.warning(f'Client send bad request. Details {str(exception.errors())}')
            return JsonResponse(
                {
                    "error": HTTP_ERRORS['bad_request'],
                    "details": exception.errors()
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
