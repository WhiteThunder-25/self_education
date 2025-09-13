from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """ Создаем модель пользователя """

    email = models.EmailField(max_length=150, unique=True, verbose_name="Email", help_text="Введите email")
    username = None
    first_name = models.CharField(max_length=30, verbose_name="Имя", help_text="Ваше имя", **NULLABLE)
    last_name = models.CharField(max_length=30, verbose_name="Фамилия", help_text="Ваша фамилия", **NULLABLE)
    phone_number = PhoneNumberField(max_length=12, verbose_name="Телефон", help_text="Ваш номер телефона", **NULLABLE)
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", help_text="Ваше фото", **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
