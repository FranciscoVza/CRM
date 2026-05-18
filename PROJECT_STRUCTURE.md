CRM Django - Estructura Completa del Proyecto
================================================

crm1/
│
├── crm_project/                    # Configuración del proyecto Django
│   ├── __init__.py
│   ├── settings.py                 # Configuración principal
│   ├── urls.py                     # URLs del proyecto
│   ├── wsgi.py                     # WSGI para producción
│   └── asgi.py                     # ASGI para WebSockets (futuro)
│
├── apps/                           # Aplicaciones Django
│   │
│   ├── accounts/                   # Gestión de usuarios y cuentas
│   │   ├── models.py               # User, Account, AccountUser, Profile
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   ├── contacts/                   # Gestión de contactos
│   │   ├── models.py               # Contact, ContactLabel, ContactActivity
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   ├── conversations/              # Gestión de conversaciones/tickets
│   │   ├── models.py               # Conversation, Message, ConversationActivity
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   ├── agents/                     # Gestión de agentes
│   │   ├── models.py               # Agent, AgentSkill, AgentShift
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   ├── teams/                      # Gestión de equipos
│   │   ├── models.py               # Team, TeamMember
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   ├── channels/                   # Canales de comunicación
│   │   ├── models.py               # Channel, ChannelWebWidget
│   │   ├── views.py                # Vistas API
│   │   ├── serializers.py          # Serializadores
│   │   ├── admin.py                # Panel de admin
│   │   ├── urls.py                 # URLs de la app
│   │   ├── apps.py                 # Configuración de app
│   │   └── __init__.py
│   │
│   └── dashboard/                  # Panel de control y reportes
│       ├── models.py               # DashboardReport, DashboardMetric
│       ├── views.py                # Vistas API para estadísticas
│       ├── serializers.py          # Serializadores
│       ├── admin.py                # Panel de admin
│       ├── urls.py                 # URLs de la app
│       ├── apps.py                 # Configuración de app
│       └── __init__.py
│
├── templates/                      # Plantillas HTML (si se necesita)
│
├── static/                         # Archivos estáticos (CSS, JS, imágenes)
│
├── media/                          # Archivos subidos por usuarios
│
├── manage.py                       # Comando de Django
│
├── requirements.txt                # Dependencias Python
│
├── .env.example                    # Ejemplo de variables de entorno
│
├── .gitignore                      # Archivos ignorados por Git
│
├── README.md                       # Documentación principal
│
├── QUICK_START.md                  # Guía de inicio rápido
│
├── ADVANCED_GUIDE.md               # Guía avanzada y configuración
│
├── Dockerfile                      # Docker para containerizar
│
├── docker-compose.yml              # Docker Compose para desarrollo
│
├── gunicorn_config.py              # Configuración de Gunicorn
│
├── nginx.conf                      # Configuración de Nginx
│
├── deploy.sh                       # Script de despliegue
│
├── crm.service                     # Servicio systemd para Django
│
├── crm-celery.service              # Servicio systemd para Celery Worker
│
├── crm-celery-beat.service         # Servicio systemd para Celery Beat
│
└── tests.py                        # Tests unitarios


RUTAS API DISPONIBLES
=====================

Autenticación:
  POST   /api/token/
  POST   /api/token/refresh/

Cuentas y Usuarios:
  GET    /api/v1/accounts/users/
  POST   /api/v1/accounts/users/
  GET    /api/v1/accounts/users/{id}/
  PUT    /api/v1/accounts/users/{id}/
  DELETE /api/v1/accounts/users/{id}/
  GET    /api/v1/accounts/users/me/
  GET    /api/v1/accounts/users/{id}/profile/
  PUT    /api/v1/accounts/users/{id}/update_profile/

  GET    /api/v1/accounts/accounts/
  POST   /api/v1/accounts/accounts/
  GET    /api/v1/accounts/accounts/{id}/members/
  POST   /api/v1/accounts/accounts/{id}/add_member/
  POST   /api/v1/accounts/accounts/{id}/remove_member/

Contactos:
  GET    /api/v1/contacts/contacts/
  POST   /api/v1/contacts/contacts/
  GET    /api/v1/contacts/contacts/{id}/
  PUT    /api/v1/contacts/contacts/{id}/
  DELETE /api/v1/contacts/contacts/{id}/
  POST   /api/v1/contacts/contacts/{id}/add_label/
  POST   /api/v1/contacts/contacts/{id}/remove_label/
  POST   /api/v1/contacts/contacts/{id}/add_activity/

  GET    /api/v1/contacts/labels/
  POST   /api/v1/contacts/labels/

  GET    /api/v1/contacts/segments/
  POST   /api/v1/contacts/segments/

Conversaciones:
  GET    /api/v1/conversations/conversations/
  POST   /api/v1/conversations/conversations/
  GET    /api/v1/conversations/conversations/{id}/
  PUT    /api/v1/conversations/conversations/{id}/
  POST   /api/v1/conversations/conversations/{id}/assign/
  POST   /api/v1/conversations/conversations/{id}/change_status/
  POST   /api/v1/conversations/conversations/{id}/change_priority/
  POST   /api/v1/conversations/conversations/{id}/add_label/
  POST   /api/v1/conversations/conversations/{id}/remove_label/

  GET    /api/v1/conversations/messages/
  POST   /api/v1/conversations/messages/
  GET    /api/v1/conversations/messages/{id}/

  GET    /api/v1/conversations/notes/
  POST   /api/v1/conversations/notes/

  GET    /api/v1/conversations/labels/
  POST   /api/v1/conversations/labels/

Agentes:
  GET    /api/v1/agents/agents/
  GET    /api/v1/agents/agents/{id}/
  POST   /api/v1/agents/agents/{id}/change_availability/
  POST   /api/v1/agents/agents/{id}/add_skill/
  POST   /api/v1/agents/agents/{id}/remove_skill/
  POST   /api/v1/agents/agents/{id}/add_shift/

Equipos:
  GET    /api/v1/teams/teams/
  POST   /api/v1/teams/teams/
  GET    /api/v1/teams/teams/{id}/
  PUT    /api/v1/teams/teams/{id}/
  POST   /api/v1/teams/teams/{id}/add_member/
  POST   /api/v1/teams/teams/{id}/remove_member/

Canales:
  GET    /api/v1/channels/channels/
  POST   /api/v1/channels/channels/
  GET    /api/v1/channels/channels/{id}/
  PUT    /api/v1/channels/channels/{id}/
  DELETE /api/v1/channels/channels/{id}/
  POST   /api/v1/channels/channels/{id}/test_connection/
  POST   /api/v1/channels/channels/{id}/sync_now/
  GET    /api/v1/channels/channels/{id}/widget/
  POST   /api/v1/channels/channels/{id}/widget/
  PUT    /api/v1/channels/channels/{id}/widget/

Dashboard:
  GET    /api/v1/dashboard/reports/
  POST   /api/v1/dashboard/reports/

  GET    /api/v1/dashboard/stats/overview/
  GET    /api/v1/dashboard/stats/conversation_metrics/
  GET    /api/v1/dashboard/stats/agent_performance/
  GET    /api/v1/dashboard/stats/channel_breakdown/

Documentación:
  GET    /api/schema/           (Swagger UI)
  GET    /api/redoc/            (ReDoc)


MODELOS DE DATOS PRINCIPALES
=============================

User
  - email (unique)
  - username (unique)
  - first_name
  - last_name
  - password
  - avatar (imagen)
  - phone
  - location
  - is_staff / is_active

Account (Organización)
  - name
  - slug (unique)
  - description
  - logo (imagen)
  - owner (FK User)
  - plan (free/starter/professional/enterprise)
  - active
  - domain

AccountUser (Rol en Cuenta)
  - account (FK Account)
  - user (FK User)
  - role (admin/agent/manager)

Contact (Cliente)
  - account (FK Account)
  - email
  - phone
  - name
  - avatar
  - status (active/inactive/blocked)
  - company
  - location
  - custom_attributes (JSON)

Conversation (Ticket/Chat)
  - account (FK Account)
  - contact (FK Contact)
  - assignee (FK User)
  - subject
  - status (open/resolved/waiting/snoozed)
  - priority (low/medium/high/urgent)
  - source (email/chat/whatsapp/instagram/etc)
  - labels (M2M ContactLabel)

Message (Mensaje)
  - conversation (FK Conversation)
  - sender (FK User)
  - message_type (incoming/outgoing/activity)
  - content
  - attachments (JSON)
  - sent_at / read_at

Agent (Perfil de Agente)
  - account (O2O AccountUser)
  - availability (online/busy/away/offline)
  - max_conversations
  - current_conversations
  - skills (M2M)

Team (Equipo)
  - account (FK Account)
  - name
  - members (M2M User through TeamMember)

Channel (Canal de Comunicación)
  - account (FK Account)
  - channel_type (email/chat/whatsapp/etc)
  - credentials (JSON - encriptado)
  - is_active
  - sync_enabled


VARIABLES DE ENTORNO
====================

DEBUG=True                          # Modo debug (False en producción)
SECRET_KEY=...                      # Clave secreta
ALLOWED_HOSTS=localhost,127.0.0.1  # Hosts permitidos

DB_ENGINE=django.db.backends.postgresql
DB_NAME=crm_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=user@gmail.com
EMAIL_HOST_PASSWORD=password

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

