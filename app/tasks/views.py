from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'created_at']
    ordering_fields = ['created_at', 'updated_at']

    def retrieve(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        cache_key = f"task_{task_id}"
        print(f"Шукаємо кеш для task_{task_id}")
        cached_data = cache.get(cache_key)

        if cached_data:
            print(f"Отримано дані з кешу для task_{task_id}")
            return Response(cached_data)

        print(f"Дані не знайдені в кеші, отримання з бази даних для task_{task_id}")
        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)
        print(f"Зберігаємо дані в кеш для task_{task_id}")
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete_pattern("task_*")
        print("Кеш усіх задач видалено після створення нової")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        task_id = kwargs['pk']
        cache.delete(f"task_{task_id}")
        print(f"Кеш для task_{task_id} видалено після оновлення")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        task_id = kwargs['pk']
        cache.delete(f"task_{task_id}")
        print(f"Кеш для task_{task_id} видалено після видалення")
        return response
