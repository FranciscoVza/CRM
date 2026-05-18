from django.db import models
from apps.accounts.models import Account, User
from apps.contacts.models import Contact
from django.utils.translation import gettext_lazy as _


class Conversation(models.Model):
    STATUS_CHOICES = (
        ('open', 'Abierta'),
        ('resolved', 'Resuelta'),
        ('waiting', 'En Espera'),
        ('snoozed', 'Pospuesta'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='conversations')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='conversations')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_conversations')

    subject = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    source = models.CharField(max_length=50)  # 'email', 'chat', 'whatsapp', 'twitter', etc.
    channel_id = models.CharField(max_length=255, blank=True)  # Reference to channel source ID

    labels = models.ManyToManyField('ConversationLabel', blank=True, related_name='conversations')

    # Metadata
    first_response_at = models.DateTimeField(null=True, blank=True)
    last_message_at = models.DateTimeField(null=True, blank=True)
    resolution_time = models.IntegerField(null=True, blank=True)  # in minutes
    waiting_since = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Conversación')
        verbose_name_plural = _('Conversaciones')
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['account', 'status']),
            models.Index(fields=['assignee', 'status']),
        ]

    def __str__(self):
        return f'{self.subject} - {self.contact.name}'


class ConversationLabel(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='conversation_labels')
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7, default='#3498db')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['account', 'name']
        verbose_name = _('Etiqueta de Conversación')
        verbose_name_plural = _('Etiquetas de Conversación')

    def __str__(self):
        return self.name


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = (
        ('incoming', 'Entrante'),
        ('outgoing', 'Saliente'),
        ('activity', 'Actividad'),
    )

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_messages')
    sender_name = models.CharField(max_length=255)  # For incoming messages from contacts

    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()

    # Attachments
    attachments = models.JSONField(default=list, blank=True)  # Store file URLs/metadata

    # For outgoing messages
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    # External message tracking
    external_id = models.CharField(max_length=255, blank=True)  # For API integrations

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Mensaje')
        verbose_name_plural = _('Mensajes')
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
        ]

    def __str__(self):
        return f'{self.sender_name} - {self.conversation.subject}'


class ConversationActivity(models.Model):
    ACTIVITY_TYPES = (
        ('assigned', 'Asignado'),
        ('status_change', 'Cambio de Estado'),
        ('priority_change', 'Cambio de Prioridad'),
        ('label_added', 'Etiqueta Añadida'),
        ('label_removed', 'Etiqueta Removida'),
        ('note_added', 'Nota Añadida'),
    )

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    description = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Actividad de Conversación')
        verbose_name_plural = _('Actividades de Conversación')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_activity_type_display()} - {self.conversation.subject}'


class ConversationNote(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Nota de Conversación')
        verbose_name_plural = _('Notas de Conversación')
        ordering = ['-created_at']

    def __str__(self):
        return f'Nota - {self.conversation.subject}'
