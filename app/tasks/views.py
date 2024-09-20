from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response

class TaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'priority', 'created_at']
    ordering_fields = ['created_at', 'updated_at']
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by task status", type=openapi.TYPE_STRING),
            openapi.Parameter('priority', openapi.IN_QUERY, description="Filter by task priority", type=openapi.TYPE_STRING),
            openapi.Parameter('created_at', openapi.IN_QUERY, description="Filter by task creation date", type=openapi.TYPE_STRING),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by created_at or updated_at", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        task_id = kwargs['pk']
        cache_key = f"task_{task_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        response = super().retrieve(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60*5)
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        cache.delete_pattern("task_*")
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        task_id = kwargs['pk']
        cache.delete(f"task_{task_id}")
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        task_id = kwargs['pk']
        cache.delete(f"task_{task_id}")
        return response
