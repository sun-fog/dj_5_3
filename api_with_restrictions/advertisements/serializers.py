# serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from advertisements.models import Advertisement
from advertisements.models import AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериализатор для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания объявления."""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """
        Метод для валидации. Вызывается при создании и обновлении.
        Проверяет:
        - Не более 10 открытых объявлений у пользователя (при создании).
        - При обновлении — что пользователь является автором (если меняется статус).
        """
        user = self.context['request'].user

        # Проверка при создании нового объявления
        if self.instance is None:
            open_count = Advertisement.objects.filter(
                creator=user,
                status=AdvertisementStatusChoices.OPEN
            ).count()
            if open_count >= 10:
                raise ValidationError("У вас уже есть 10 открытых объявлений.")

        # Проверка при обновлении (если меняется статус)
        else:
            if 'status' in data:
                if self.instance.creator != user:
                    raise ValidationError("Вы не можете изменять статус чужого объявления.")

        return data
