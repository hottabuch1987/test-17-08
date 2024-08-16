from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers
from courses.models import Course, Group, Lesson
from users.models import Subscription
from .user_serializer import CustomUserSerializer


User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""

    # TODO Доп. задание
    users = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (  
            'title',
            'course',
            'users',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""
    

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
            'users',
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

   
    lessons = MiniLessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lessons.count()
        # TODO Доп. задание

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        # TODO Доп. задание
        return obj.cours_groups.aggregate(total_students=Count('users'))['total_students'] or 0

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 10 чел.."""
        total_groups = obj.cours_groups.count()
        total_students = self.get_students_count(obj)
        max_group_size = 10
        filled_groups = (total_students + max_group_size - 1) // max_group_size  # Округляем вверх
        filled_percent = (filled_groups / total_groups * 100) if total_groups > 0 else 0
        return round(filled_percent, 2)
        
        # TODO Доп. задание

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        # TODO Доп. задание
        total_subscriptions = Subscription.objects.filter(course=obj, active=True).count()  # Количество активных подписок
        if total_subscriptions == 0:
            return 0.0  # Если нет подписок, вернем 0%
        total_purchases = Subscription.objects.filter(course=obj).count()  # Общее количество подписок на курс
        demand_percent = (total_subscriptions / total_purchases * 100) if total_purchases > 0 else 0
        return round(demand_percent, 2)

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
            'is_available',
          
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = (
            'title',
            'author',
            'price',
            'start_date',
        )
