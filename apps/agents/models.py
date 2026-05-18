from django.db import models
from apps.accounts.models import Account, User, AccountUser
from django.utils.translation import gettext_lazy as _


class Agent(models.Model):
    AVAILABILITY_CHOICES = (
        ('online', 'En línea'),
        ('busy', 'Ocupado'),
        ('away', 'Ausente'),
        ('offline', 'Desconectado'),
    )

    account = models.OneToOneField(AccountUser, on_delete=models.CASCADE, related_name='agent_profile')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='offline')
    auto_assignment = models.BooleanField(default=True)
    max_conversations = models.IntegerField(default=20)
    current_conversations = models.IntegerField(default=0)

    # Statistics
    total_conversations = models.IntegerField(default=0)
    resolved_conversations = models.IntegerField(default=0)
    average_response_time = models.IntegerField(default=0)  # in seconds

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Agente')
        verbose_name_plural = _('Agentes')

    def __str__(self):
        return f'{self.account.user.email} - {self.account.account.name}'


class AgentSkill(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=255)
    level = models.IntegerField(choices=[(i, f'Nivel {i}') for i in range(1, 6)], default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['agent', 'name']
        verbose_name = _('Habilidad de Agente')
        verbose_name_plural = _('Habilidades de Agentes')

    def __str__(self):
        return f'{self.agent.account.user.email} - {self.name}'


class AgentShift(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='shifts')
    day_of_week = models.IntegerField(choices=[(i, ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][i]) for i in range(7)])
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Turno de Agente')
        verbose_name_plural = _('Turnos de Agentes')

    def __str__(self):
        return f'{self.agent.account.user.email} - Turno'


class AgentStatistics(models.Model):
    agent = models.OneToOneField(Agent, on_delete=models.CASCADE, related_name='statistics')
    conversations_handled = models.IntegerField(default=0)
    average_resolution_time = models.IntegerField(default=0)  # in minutes
    customer_satisfaction_score = models.FloatField(default=0)  # 0-5
    messages_sent = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Estadística de Agente')
        verbose_name_plural = _('Estadísticas de Agentes')

    def __str__(self):
        return f'Estadísticas de {self.agent.account.user.email}'
