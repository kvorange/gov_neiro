from pydantic import BaseModel, constr


class RegistrationBody(BaseModel):
    login: constr(max_length=100)
    password: str
    name: constr(max_length=100)

class LoginBody(BaseModel):
    login: constr(max_length=100)
    password: str
