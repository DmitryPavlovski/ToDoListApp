from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    """Model class Task object"""
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=350)
    description = models.TextField(verbose_name='Description', null=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
