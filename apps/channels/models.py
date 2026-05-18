from django.db import models
from apps.accounts.models import Account
from django.utils.translation import gettext_lazy as _


class Channel(models.Model):
    CHANNEL_TYPES = (
        ('email', 'Email'),
        ('chat', 'Chat Web'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('telegram', 'Telegram'),
        ('custom', 'Personalizado'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='channels')
    name = models.CharField(max_length=255)
    channel_type = models.CharField(max_length=50, choices=CHANNEL_TYPES)

    # Credentials and configuration
    credentials = models.JSONField(default=dict)  # Store sensitive config encrypted
    is_active = models.BooleanField(default=True)

    # Integration metadata
    external_account_id = models.CharField(max_length=255, blank=True)
    sync_enabled = models.BooleanField(default=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['account', 'name']
        verbose_name = _('Canal')
        verbose_name_plural = _('Canales')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_channel_type_display()})'


class ChannelTeamAssignment(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='team_assignments')
    team = models.ForeignKey('teams.Team', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['channel', 'team']
        verbose_name = _('Asignación de Canal a Equipo')
        verbose_name_plural = _('Asignaciones de Canales a Equipos')

    def __str__(self):
        return f'{self.channel.name} - {self.team.name}'


class ChannelWebWidget(models.Model):
    channel = models.OneToOneField(Channel, on_delete=models.CASCADE, related_name='widget', limit_choices_to={'channel_type': 'chat'})

    # Widget customization
    title = models.CharField(max_length=255, default='¿Cómo podemos ayudarte?')
    welcome_message = models.TextField(default='Bienvenido a nuestro chat de soporte')
    widget_color = models.CharField(max_length=7, default='#3498db')
    position = models.CharField(max_length=20, choices=[('left', 'Izquierda'), ('right', 'Derecha')], default='right')

    enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Widget de Chat Web')
        verbose_name_plural = _('Widgets de Chat Web')

    def __str__(self):
        return f'Widget - {self.channel.name}'
