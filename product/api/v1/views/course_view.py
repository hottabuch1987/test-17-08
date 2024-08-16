from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def perform_create(self, serializer):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        serializer.save(course=course)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return course.cours_groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы"""

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        course = get_object_or_404(Course, id=pk)
        serializer = SubscriptionSerializer(data={'user': request.user.id, 'course': course.id})
    
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # Вызов метода создания подписки
            groups = course.cours_groups.all()
            if groups.exists():
                group = groups.order_by('?').first()  # Выбор случайной группы
                group.users.add(request.user)  # Добавление пользователя в группу

        return Response({"message": "Доступ к курсу открыт!"}, status=status.HTTP_201_CREATED)


    @action(
        methods=['get'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated]
    )

    def available(self, request):
        """Получить продукты, доступные для покупки."""
        # Получаем курсы, на которые у пользователя уже есть подписки
        purchased_courses = Subscription.objects.filter(user=request.user).values_list('course', flat=True)
        # Получаем доступные курсы, исключая уже купленные
        available_courses = Course.objects.exclude(id__in=purchased_courses).filter(is_available=True)
        # Сериализуем доступные курсы
        serializer = CourseSerializer(available_courses, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

