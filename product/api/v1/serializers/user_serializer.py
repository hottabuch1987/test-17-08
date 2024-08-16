from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.db import transaction
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    # TODO

    class Meta:
        model = Subscription
        fields = (
            'user', 'course', 'subscribed_on', 'active'
        )
    

    def create(self, validated_data):
        user = validated_data['user']
        course = validated_data['course']
        # Проверка баланса пользователя
        balance = user.balance.amount
        if balance < course.price:
            raise serializers.ValidationError("Недостаточно бонусов для оплаты курса.")

        with transaction.atomic():
            # Списание бонусов
            user.balance.amount -= course.price
            user.balance.save()
            # Создание подписки
            subscription = super().create(validated_data)

        return subscription


    def assign_to_group(self, user, course):
        """Распределяет пользователя в одну из 10 групп."""

        groups = course.groups.all() 
        if groups.exists():
            group = groups.order_by('?').first()  # Выбор случайной группы
            return group
        return None


