# CRM - Sistema de Gestión de Relaciones con Clientes

Un CRM completo similar a ChatWoot construido con Django REST Framework. Este sistema permite gestionar conversaciones, contactos, agentes, equipos y múltiples canales de comunicación.

## Características Principales

- **Gestión de Conversaciones**: Crea, asigna y seguimiento de conversaciones/tickets
- **Gestión de Contactos**: Base de datos completa de clientes con actividades y etiquetas
- **Multi-Canal**: Soporte para Email, Chat Web, WhatsApp, Instagram, Twitter, Facebook, etc.
- **Gestión de Agentes**: Perfiles de agentes con habilidades, turnos y estadísticas
- **Gestión de Equipos**: Organiza agentes en equipos
- **Dashboard**: Panel de control con estadísticas y reportes
- **Autenticación JWT**: Seguridad con tokens JWT
- **API REST**: API completa documentada con Swagger/OpenAPI

## Estructura del Proyecto

```
crm1/
├── crm_project/           # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                  # Aplicaciones Django
│   ├── accounts/          # Usuarios y cuentas
│   ├── contacts/          # Gestión de contactos
│   ├── conversations/     # Gestión de conversaciones
│   ├── agents/            # Gestión de agentes
│   ├── teams/             # Gestión de equipos
│   ├── channels/          # Canales de comunicación
│   └── dashboard/         # Panel de control y reportes
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

## Requisitos

- Python 3.8+
- PostgreSQL 12+
- Redis 6+ (para Celery)
- pip

## Instalación

### 1. Clonar el repositorio y crear entorno virtual

```bash
cd crm1
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

### 4. Crear base de datos

```bash
# Asegúrate de que PostgreSQL está corriendo
# Luego crea la base de datos:
createdb crm_db
```

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## Endpoints API

### Autenticación
- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token

### Cuentas y Usuarios
- `GET/POST /api/v1/accounts/users/` - Usuarios
- `GET /api/v1/accounts/users/me/` - Información del usuario actual
- `GET/POST /api/v1/accounts/accounts/` - Cuentas

### Contactos
- `GET/POST /api/v1/contacts/contacts/` - Contactos
- `GET/POST /api/v1/contacts/labels/` - Etiquetas de contactos
- `GET/POST /api/v1/contacts/segments/` - Segmentos

### Conversaciones
- `GET/POST /api/v1/conversations/conversations/` - Conversaciones
- `GET/POST /api/v1/conversations/messages/` - Mensajes
- `GET/POST /api/v1/conversations/notes/` - Notas
- `GET/POST /api/v1/conversations/labels/` - Etiquetas

### Agentes
- `GET /api/v1/agents/agents/` - Lista de agentes
- `POST /api/v1/agents/agents/{id}/assign/` - Asignar conversación

### Equipos
- `GET/POST /api/v1/teams/teams/` - Equipos
- `POST /api/v1/teams/teams/{id}/add_member/` - Añadir miembro

### Canales
- `GET/POST /api/v1/channels/channels/` - Canales

### Dashboard
- `GET /api/v1/dashboard/stats/overview/` - Estadísticas generales
- `GET /api/v1/dashboard/stats/conversation_metrics/` - Métricas de conversaciones
- `GET /api/v1/dashboard/stats/agent_performance/` - Desempeño de agentes

## Documentación API

La documentación interactiva de la API está disponible en:
- Swagger UI: `http://localhost:8000/api/schema/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Panel de Administración

Accede al panel de administración en `http://localhost:8000/admin/` con las credenciales del superusuario.

## Modelos Principales

### Account
Representa una organización o cuenta

### User
Usuario del sistema con soporte para múltiples cuentas

### Contact
Cliente/contacto en la plataforma

### Conversation
Conversación/ticket entre un agente y un contacto

### Message
Mensaje individual dentro de una conversación

### Agent
Perfil de agente con habilidades y disponibilidad

### Team
Equipo de agentes

### Channel
Canal de comunicación (Email, WhatsApp, etc.)

## Operaciones Comunes

### Crear una cuenta
```bash
curl -X POST http://localhost:8000/api/v1/accounts/accounts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Empresa",
    "slug": "mi-empresa",
    "plan": "professional"
  }'
```

### Crear un contacto
```bash
curl -X POST http://localhost:8000/api/v1/contacts/contacts/?account_id=1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+34612345678",
    "company": "Acme Corp"
  }'
```

### Crear una conversación
```bash
curl -X POST http://localhost:8000/api/v1/conversations/conversations/?account_id=1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Soporte técnico",
    "description": "Usuario reporta problema de login",
    "contact": 1,
    "source": "email",
    "priority": "high"
  }'
```

## Desarrollo

### Ejecutar tests
```bash
python manage.py test
```

### Generar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario adicional
```bash
python manage.py createsuperuser
```

## Configuración de Celery (Tareas Asincrónicas)

Para usar Celery con Redis:

```bash
# Terminal 1 - Celery Worker
celery -A crm_project worker -l info

# Terminal 2 - Celery Beat (Tareas programadas)
celery -A crm_project beat -l info
```

## Configuración de CORS

Por defecto, CORS está configurado para `localhost:3000` y `localhost:8000`. Para agregar más orígenes:

Edita `crm_project/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://tudominio.com",
]
```

## Seguridad

- Cambia `SECRET_KEY` en `.env` en producción
- Asegúrate de que `DEBUG=False` en producción
- Usa variables de entorno para credenciales
- Configura HTTPS en producción
- Usa una base de datos segura (PostgreSQL recomendado)

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## Soporte

Para reportar bugs o sugerir mejoras, abre un issue en el repositorio.

## Roadmap

- [ ] WebSocket para actualizaciones en tiempo real
- [ ] Integración completa de canales (WhatsApp, Telegram, etc.)
- [ ] Sistema de automatización (flujos)
- [ ] Encuestas de satisfacción
- [ ] Base de conocimiento (FAQ)
- [ ] Chatbot IA
- [ ] Exportación de reportes en PDF/Excel
- [ ] Aplicación móvil
