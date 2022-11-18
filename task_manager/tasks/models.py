from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
# Create your models here.


class Task(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='author')
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="tasks")
    labels = models.ManyToManyField(Label, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
