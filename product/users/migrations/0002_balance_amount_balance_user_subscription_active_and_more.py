# Generated by Django 4.2.10 on 2024-08-16 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_lesson_course_alter_course_author'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10, verbose_name='Баланс'),
        ),
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активная подписка'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.course', verbose_name='Курс'),
        ),
        migrations.AddField(
            model_name='subscription',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
