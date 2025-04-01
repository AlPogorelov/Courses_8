from habit.models import Habit
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsOwner, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from habit.pagination import HabitPagination
from habit.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.user_owner = self.request.user
        new_habit.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]

        elif self.action == 'update' or 'partial_update' or 'destroy':
            self.permission_classes = [IsOwner]

        elif self.action == 'list_public':
            self.permission_classes = [AllowAny]

        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        # Фильтрация для разных сценариев
        if self.action == 'list_public':
            return Habit.objects.filter(is_public=True)
        if self.request.user.is_authenticated:
            return Habit.objects.filter(user=self.request.user_owner)
        return Habit.objects.none()

    @action(detail=False, methods=['get'], url_path='public')
    def list_public(self, request):
        # Получаем отфильтрованный кверисет
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request):
        queryset = Habit.objects.all()
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)
