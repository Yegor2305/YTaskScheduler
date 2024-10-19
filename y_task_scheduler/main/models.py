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
    resources = models.ManyToManyField('Resource', through="TaskResources", related_name="tasks")

    def __str__(self):
        return f"{self.name}"

class Color(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.value}"

class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return f"{self.name}"

class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name}"

class TaskResources(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.task} - {self.resource}"