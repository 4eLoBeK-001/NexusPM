import random

from django.db import models

from users.models import TeamMember


def get_colors():
    return ['sky', 'blue', 'red', 'orange', 'lime', 'teal', 'violet', 'zinc']

def get_random_color():
    return random.choice(get_colors())

class Team(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    author = models.ForeignKey('users.User', on_delete=models.SET_NULL, related_name='author_teams', null=True)
    team_member = models.ManyToManyField('users.User', through='users.TeamMember', related_name='member_teams', blank=True)

    image = models.ImageField(upload_to='team_avatars/', blank=True, null=True)
    color = models.CharField(max_length=10, default=get_random_color)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', 'name')
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    @property
    def short_name(self):
        return self.name[:2].upper()

    def __str__(self):
        return f'Пороект - {self.name}'


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
    invited_by = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='team_invitations')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'
    
    def __str__(self):
        return f'{self.invited_user} приглашён {self.invited_by} в {self.team}'

