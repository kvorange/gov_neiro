from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from server.errors.http_errors import HTTP_ERRORS
from .schemas.auth import RegistrationBody, LoginBody
from ..models import Person


@api_view(['POST'])
def registration(request: Request):
    req_body: RegistrationBody = RegistrationBody.model_validate(request.data)
    if Person.objects.filter(login=req_body.login).first():
        return Response({'error': HTTP_ERRORS['user_exists']}, status=status.HTTP_400_BAD_REQUEST)
    token = Person.registration(req_body.login, req_body.password, req_body.name)
    return Response({'token': token})


@api_view(['POST'])
def login(request: Request):
    req_body: LoginBody = LoginBody.model_validate(request.data)
    person: Person = Person.auth(req_body.login, req_body.password)
    if not person:
        return Response({'error': HTTP_ERRORS['bad_login']}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"person": person.get_info()}, status=status.HTTP_200_OK)
