from django.db import models
from apps.accounts.models import Account
from django.utils.translation import gettext_lazy as _


class Contact(models.Model):
    STATUS_CHOICES = (
        ('active', 'Activo'),
        ('inactive', 'Inactivo'),
        ('blocked', 'Bloqueado'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contacts')
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='contact_avatars/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    description = models.TextField(blank=True)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    custom_attributes = models.JSONField(default=dict, blank=True)

    # Metadata
    last_activity = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['account', 'email']
        verbose_name = _('Contacto')
        verbose_name_plural = _('Contactos')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['account', 'email']),
            models.Index(fields=['account', 'status']),
        ]

    def __str__(self):
        return f'{self.name} ({self.email})'


class ContactLabel(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contact_labels')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#3498db')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['account', 'name']
        verbose_name = _('Etiqueta de Contacto')
        verbose_name_plural = _('Etiquetas de Contacto')

    def __str__(self):
        return self.name


class ContactLabelAssignment(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='labels')
    label = models.ForeignKey(ContactLabel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['contact', 'label']
        verbose_name = _('Asignación de Etiqueta')
        verbose_name_plural = _('Asignaciones de Etiqueta')


class ContactActivity(models.Model):
    ACTIVITY_TYPES = (
        ('email', 'Email'),
        ('call', 'Llamada'),
        ('meeting', 'Reunión'),
        ('note', 'Nota'),
        ('task', 'Tarea'),
        ('custom', 'Personalizada'),
    )

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = _('Actividad de Contacto')
        verbose_name_plural = _('Actividades de Contacto')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_activity_type_display()} - {self.title}'


class ContactSegment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contact_segments')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    query = models.JSONField()  # Define rules for segment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Segmento de Contacto')
        verbose_name_plural = _('Segmentos de Contacto')

    def __str__(self):
        return self.name
