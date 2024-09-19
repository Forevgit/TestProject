from django.db import models
from enum import Enum
from django.utils.translation import gettext_lazy as _

class StatusEnum(Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace("_", " ").title()) for key in cls]


class PriorityEnum(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]


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

    def __str__(self):
        return self.title
