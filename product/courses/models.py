from django.db import models
from users.models import Subscription


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        default=1 
        
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, 
        verbose_name='Стоимость',
        default=0.00,
    )

    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    is_available = models.BooleanField(
        default=True, 
        verbose_name='Доступен для покупки'
    )


    # TODO
    def has_access(self, user):
        """Проверка доступа пользователя к курсу."""
        return Subscription.objects.filter(user=user, course=self).exists()


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title
    



class Lesson(models.Model):
    """Модель урока."""
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
        default=1,
    )

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    # TODO

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""
    title = models.CharField(
        max_length=250,
        verbose_name='Название группы',
    )
    users = models.ManyToManyField(
        'users.CustomUser',
        related_name='user_groups',
        verbose_name='Студенты',
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, 
        related_name='cours_groups',
        verbose_name='Курс',
    )
    def __str__(self):
        return self.title

    # TODO

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
