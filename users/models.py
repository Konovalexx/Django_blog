from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.conf import settings

class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/avatars/',
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Страна",
    )
    email_verified = models.BooleanField(default=False, verbose_name="Email верифицирован")
    email_verification_token = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        verbose_name="Токен для верификации email",
    )

    def send_verification_email(self):
        # Генерация ссылки для верификации
        verification_link = f"{settings.SITE_URL}/users/verify-email/{self.pk}/{self.email_verification_token}/"
        send_mail(
            'Подтвердите ваш email',
            f'Пожалуйста, подтвердите ваш email, перейдя по следующей ссылке: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
        )

    def generate_verification_token(self):
        token = get_random_string(32)
        self.email_verification_token = token
        self.save()  # Сохраняем токен в базе данных
        return token