# Guía Avanzada de CRM Django

## Autenticación y Autorización

### JWT (JSON Web Tokens)

El CRM utiliza JWT para autenticación. El flujo es:

1. Usuario obtiene token con credenciales
2. Incluye token en header Authorization: Bearer {token}
3. Token tiene expiración configurable

### Permisos y Roles

- **Admin**: Acceso total a la cuenta
- **Manager**: Puede gestionar agentes y equipos
- **Agent**: Acceso limitado a conversaciones asignadas

## Integración de Canales

### Email

```python
# Configurar IMAP para recibir emails
CHANNEL_CONFIG = {
    'channel_type': 'email',
    'credentials': {
        'imap_server': 'imap.gmail.com',
        'imap_port': 993,
        'email': 'noreply@empresa.com',
        'password': 'app_password',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
    }
}
```

### WhatsApp (ejemplo con Twilio)

```python
CHANNEL_CONFIG = {
    'channel_type': 'whatsapp',
    'credentials': {
        'account_sid': 'YOUR_ACCOUNT_SID',
        'auth_token': 'YOUR_AUTH_TOKEN',
        'phone_number': '+1234567890',
    }
}
```

## Automatizaciones y Workflows

### Crear Workflow de Asignación Automática

```python
from apps.conversations.models import Conversation

# Cuando se crea una conversación, asignarla automáticamente
@receiver(post_save, sender=Conversation)
def auto_assign_conversation(sender, instance, created, **kwargs):
    if created and not instance.assignee:
        # Lógica para encontrar agente disponible
        available_agent = get_available_agent(instance.account)
        if available_agent:
            instance.assignee = available_agent
            instance.save()
```

## Reportes Personalizados

### Crear Reporte de Conversaciones por Agente

```python
from django.db.models import Count, Avg
from apps.conversations.models import Conversation

def get_agent_performance_report(account_id, start_date, end_date):
    report = Conversation.objects.filter(
        account_id=account_id,
        created_at__range=[start_date, end_date]
    ).values('assignee__email').annotate(
        total=Count('id'),
        resolved=Count('id', filter=Q(status='resolved')),
        avg_time=Avg('resolution_time')
    )
    return report
```

## API Webhooks

### Recibir eventos de canales externos

```python
# urls.py
path('api/webhooks/whatsapp/', WhatsAppWebhookView.as_view(), name='whatsapp-webhook'),

# views.py
class WhatsAppWebhookView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Procesar mensaje de WhatsApp
        # Crear conversación/mensaje
        return Response({'status': 'ok'})
```

## Caché y Rendimiento

### Configurar Redis para caché

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Cachear consultas frecuentes

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cachear por 5 minutos
@api_view(['GET'])
def get_dashboard_stats(request):
    # Estadísticas del dashboard
    pass
```

## Búsqueda y Filtrado Avanzado

### Filtrado personalizado

```python
# views.py
from django_filters import rest_framework as filters

class ConversationFilter(filters.FilterSet):
    created_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte'
    )

    class Meta:
        model = Conversation
        fields = ['status', 'priority', 'assignee', 'created_after', 'created_before']
```

## Auditoría y Logging

### Registrar cambios en conversaciones

```python
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

def log_conversation_change(conversation, action, user):
    LogEntry.objects.create(
        user=user,
        content_type=ContentType.objects.get_for_model(Conversation),
        object_id=conversation.pk,
        object_repr=str(conversation),
        action_flag=CHANGE,
        change_message=action
    )
```

## Notificaciones en Tiempo Real

### WebSocket con Django Channels (futuro)

```python
# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        await self.channel_layer.group_add(
            f"conversation_{self.conversation_id}",
            self.channel_name
        )
        await self.accept()

    async def new_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
```

## Backup y Recuperación

### Script de backup diario

```bash
#!/bin/bash

# Backup diario de base de datos
BACKUP_DIR="/backups/crm"
DB_NAME="crm_db"
DB_USER="postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/crm_$TIMESTAMP.sql.gz

# Backup de archivos
tar -czf $BACKUP_DIR/media_$TIMESTAMP.tar.gz /home/usuario/crm1/media/

# Limpiar backups antiguos (mantener últimos 30 días)
find $BACKUP_DIR -type f -mtime +30 -delete
```

## Monitoreo y Alertas

### Configurar alertas con Sentry

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

## Escalabilidad

### Configuración para múltiples workers

```python
# gunicorn_config.py
workers = 8  # 2-4 x CPU cores
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
```

### Balanceo de carga con Nginx

Ver archivo `nginx.conf` para configuración de upstream con múltiples servidores.

## Exportación de Datos

### Exportar conversaciones a CSV

```python
from django.http import HttpResponse
import csv

def export_conversations(request, account_id):
    conversations = Conversation.objects.filter(account_id=account_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="conversations.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Subject', 'Contact', 'Status', 'Created At'])

    for conv in conversations:
        writer.writerow([
            conv.id,
            conv.subject,
            conv.contact.name,
            conv.status,
            conv.created_at
        ])

    return response
```

## Soporte Multi-idioma

El CRM está configurado para español. Para agregar otros idiomas:

```bash
# Extrae cadenas translatable
python manage.py makemessages -l es -l en -l fr

# Traduce archivos .po
# Luego compila
python manage.py compilemessages
```

## Documentación API con Swagger

Accede a `/api/schema/` para documentación interactiva completa de todos los endpoints con ejemplos.
