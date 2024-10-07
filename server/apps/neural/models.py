import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from django.utils import timezone

from gov_neural.settings import PASSWORD_SALT


class Person(models.Model):
    login = models.CharField(max_length=100, verbose_name='Логин', unique=True)
    password = models.TextField(verbose_name='Пароль')
    name = models.CharField(max_length=100, verbose_name='Имя')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Дата регистрации')
    token = models.TextField(verbose_name='Токен', default='')
    token_create_at = models.DateTimeField(verbose_name='Дата последнего входа', default=timezone.now)

    def __str__(self):
        return self.login

    class Meta:
        db_table = 'person'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @staticmethod
    def registration(login: str, password: str, name: str) -> str:
        hash_password = make_password(password, PASSWORD_SALT)
        token = uuid.uuid4()
        new_person = Person.objects.create(
            login=login,
            password=hash_password,
            name=name,
            token=token,
            token_create_at=timezone.now(),
        )
        new_person.save()
        return new_person.token

    @staticmethod
    def auth(login: str, password: str):
        person = Person.objects.filter(login=login).first()
        if not person:
            return {}
        if not check_password(password, person.password):
            return {}
        person.token = uuid.uuid4()
        person.token_create_at = timezone.now()
        person.save()
        return person

    def get_info(self):
        return {
            'login': self.login,
            'name': self.name,
            'token': self.token,
            'token_create_at': self.token_create_at,
        }
