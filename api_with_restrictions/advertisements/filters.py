# filters.py
from django_filters import rest_framework as filters
from advertisements.models import Advertisement
from advertisements.models import AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # Фильтр по дате создания
    created_at_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lt'
    )
    created_at_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gt'
    )
    # Фильтр по статусу
    status = filters.ChoiceFilter(
        choices=AdvertisementStatusChoices.choices
    )
    # Фильтр по создателю
    creator = filters.NumberFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status', 'creator']
