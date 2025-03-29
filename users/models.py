from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, verbose_name='Телефон', blank=True, null=True,
                             help_text="Введите номер телефона")
    tg_chat_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='Телеграмм чат-id',
                                  help_text='Введите телеграмм чат-id')
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
