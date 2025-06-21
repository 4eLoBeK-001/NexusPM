from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from project_manager import settings


# Create your models here.

class User(AbstractUser):
    ...


class TeamMember(models.Model):
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joining = models.DateTimeField(auto_now_add=True)
    