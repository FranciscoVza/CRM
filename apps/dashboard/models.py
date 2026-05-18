from django.db import models
from apps.accounts.models import Account
from django.utils.translation import gettext_lazy as _


class DashboardReport(models.Model):
    REPORT_TYPES = (
        ('conversations', 'Conversaciones'),
        ('contacts', 'Contactos'),
        ('agents', 'Agentes'),
        ('channels', 'Canales'),
        ('performance', 'Desempeño'),
    )

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reports')
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField(blank=True)

    # Configuration
    filters = models.JSONField(default=dict, blank=True)
    date_range = models.CharField(max_length=50, default='30d')  # '7d', '30d', 'custom'

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Reporte del Panel')
        verbose_name_plural = _('Reportes del Panel')

    def __str__(self):
        return self.name


class DashboardMetric(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='metrics')
    metric_name = models.CharField(max_length=255)
    metric_value = models.FloatField()
    metadata = models.JSONField(default=dict, blank=True)

    date = models.DateField()

    class Meta:
        unique_together = ['account', 'metric_name', 'date']
        verbose_name = _('Métrica del Panel')
        verbose_name_plural = _('Métricas del Panel')
        ordering = ['-date']

    def __str__(self):
        return f'{self.metric_name} - {self.date}'
