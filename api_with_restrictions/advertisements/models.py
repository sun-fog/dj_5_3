# models.py
from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""

    # Заголовок
    title = models.TextField()
    # Описание
    description = models.TextField(default='')
    # Статус
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    # Создатель
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # Создано
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    # Обновлено
    updated_at = models.DateTimeField(
        auto_now=True
    )
