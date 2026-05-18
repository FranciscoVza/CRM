from django.db import models
from apps.accounts.models import Account, User
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    allow_all_conversations = models.BooleanField(default=False)
    members = models.ManyToManyField(User, through='TeamMember', related_name='teams')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['account', 'name']
        verbose_name = _('Equipo')
        verbose_name_plural = _('Equipos')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.account.name}'


class TeamMember(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Gerente'),
        ('member', 'Miembro'),
    )

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['team', 'user']
        verbose_name = _('Miembro de Equipo')
        verbose_name_plural = _('Miembros de Equipos')

    def __str__(self):
        return f'{self.user.email} - {self.team.name}'
