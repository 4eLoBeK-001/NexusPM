from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f'Пороект - {self.name}'
