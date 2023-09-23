from django.conf import settings
from django.db import models


# Create your models here.


class Task(models.Model):
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='tasks')
    team = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"<{self.title}-{self.create_user}>"


class SubTask(models.Model):
    team = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    task = models.ForeignKey("Task", on_delete=models.DO_NOTHING, related_name='subtasks')

    def __str__(self):
        return f"<{self.team}:{self.task}>"
