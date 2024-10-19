from django.db import models
from accounts.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(auto_now=True)
    time_start = models.TimeField()
    time_end = models.TimeField()
    priority = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
