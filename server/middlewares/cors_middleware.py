"""Middleware связанные с работой Pydantic."""
import logging

from django.http import JsonResponse


class CorsCustomMiddleware:
    """Middleware отлова и обработки ошибок валидации библиотеки Pydantic."""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        if request.method == 'OPTIONS':
            response = JsonResponse({}, status=200)
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = "*"
        response['Access-Control-Allow-Headers'] = "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With"
        response['Access-Control-Max-Age'] = "1728000"
        return response
