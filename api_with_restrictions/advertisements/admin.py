# admin.py
from django.contrib import admin
from advertisements.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    """Админка для модели Advertisement."""

    # Поля для отображения в списке админки
    list_display = ('title', 'creator', 'status', 'created_at')
    # Поля для фильтрации по статусу, дате создания и создателю
    list_filter = ('status', 'created_at', 'creator')
    # Поля для поиска по заголовку и описанию
    search_fields = ('title', 'description')