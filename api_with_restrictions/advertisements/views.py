# views.py
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all() # Получение всех объявлений
    serializer_class = AdvertisementSerializer # Сериализатор для объявлений
    filter_backends = (filters.DjangoFilterBackend,) # Фильтрация
    filterset_class = AdvertisementFilter # Класс фильтра
    throttle_classes = [UserRateThrottle, AnonRateThrottle] # Тротлинг для пользователей

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()] # Только авторизованные пользователи могут создавать и обновлять объявления
        return []

    def perform_create(self, serializer):
        """Создание объявления."""
        serializer.save(creator=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Удаление объявления."""
        instance = self.get_object()
        if instance.creator != request.user:
            return Response(
                {"detail": "Вы не можете удалить чужое объявление."},
                status=status.HTTP_403_FORBIDDEN # Ответ с ошибкой
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Обновление объявления."""
        instance = self.get_object()
        if instance.creator != request.user:
            return Response(
                {"detail": "Вы не можете редактировать чужое объявление."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Частичное обновление объявления."""
        instance = self.get_object()
        if instance.creator != request.user:
            return Response(
                {"detail": "Вы не можете редактировать чужое объявление."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)