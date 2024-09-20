from django.db import models
from .enum.status_enum import StatusEnum
from .enum.priority_enum import PriorityEnum



class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=StatusEnum.choices(),
        default=StatusEnum.NEW.value
    )
    priority = models.CharField(
        max_length=20,
        choices=PriorityEnum.choices(),
        default=PriorityEnum.MEDIUM.value
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
