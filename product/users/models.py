from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone



class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=1,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        verbose_name='Баланс',
    )


    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValidationError('Баланс не может быть меньше 0')
        super().save(*args, **kwargs)

    # TODO

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        default=1,
    )
    course = models.ForeignKey(
        'courses.Course', 
        on_delete=models.CASCADE,
        verbose_name='Курс',
        default=1,
        
    )
    subscribed_on = models.DateTimeField(
        verbose_name='Дата подписки',
        default=timezone.now
    )
    
    active = models.BooleanField(
        default=True,
        verbose_name='Активная подписка',
    )


    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-subscribed_on',)
        unique_together = ('user', 'course') 

    def __str__(self):
        return f'Подписка {self.user.get_full_name()} на {self.course.title}'
    
    # TODO

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

