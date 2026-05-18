# Quick Start Guide - CRM Django

Guía rápida para empezar con el CRM Django en 5 minutos.

## Opción 1: Con Docker (Recomendado)

### Requisitos
- Docker y Docker Compose instalados

### Pasos

```bash
cd crm1
docker-compose up -d
```

El sistema estará listo en:
- API: http://localhost:8000
- Admin: http://localhost:8000/admin
- Documentación: http://localhost:8000/api/schema/

Credenciales por defecto (created on first run):
- Usuario: admin
- Email: admin@example.com
- Contraseña: (generada automáticamente)

### Ver logs

```bash
docker-compose logs -f web
```

### Detener servicios

```bash
docker-compose down
```

---

## Opción 2: Instalación Local

### Requisitos
- Python 3.8+
- PostgreSQL 12+
- Redis 6+

### Pasos

1. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Edita .env según tu configuración
   ```

4. **Crear y llenar base de datos**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

6. **En otra terminal: ejecutar Celery (opcional)**
   ```bash
   celery -A crm_project worker -l info
   ```

Accede a: http://localhost:8000

---

## Uso Básico

### 1. Obtener Token de Autenticación

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your_password"}'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Crear una Cuenta

```bash
curl -X POST http://localhost:8000/api/v1/accounts/accounts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Empresa",
    "slug": "mi-empresa",
    "plan": "professional"
  }'
```

### 3. Crear un Contacto

```bash
curl -X POST http://localhost:8000/api/v1/contacts/contacts/?account_id=1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan García",
    "email": "juan@ejemplo.com",
    "phone": "+34612345678",
    "company": "Acme Corp",
    "status": "active"
  }'
```

### 4. Crear una Conversación

```bash
curl -X POST http://localhost:8000/api/v1/conversations/conversations/?account_id=1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Solicitud de soporte",
    "description": "Usuario reporta error en login",
    "contact": 1,
    "source": "email",
    "priority": "high",
    "status": "open"
  }'
```

### 5. Añadir Mensaje a Conversación

```bash
curl -X POST http://localhost:8000/api/v1/conversations/messages/?conversation_id=1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Estamos investigando el problema",
    "message_type": "outgoing"
  }'
```

### 6. Obtener Estadísticas

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard/stats/overview/?account_id=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Interfaces Web Disponibles

1. **Admin Django**: http://localhost:8000/admin/
2. **Documentación Swagger**: http://localhost:8000/api/schema/
3. **ReDoc**: http://localhost:8000/api/redoc/

---

## Comandos Útiles

```bash
# Ver todas las rutas disponibles
python manage.py show_urls

# Crear datos de prueba
python manage.py shell
# Luego ejecutar:
# from apps.accounts.models import User, Account
# user = User.objects.create_user(email='test@test.com', username='test', password='test123')
# account = Account.objects.create(name='Test', slug='test', owner=user)

# Limpiar base de datos (CUIDADO - Borra todo)
python manage.py flush

# Hacer backup de base de datos
python manage.py dumpdata > backup.json

# Restaurar desde backup
python manage.py loaddata backup.json
```

---

## Solución de Problemas

### Error: "No such table: conversations_conversation"
Ejecuta: `python manage.py migrate`

### Error: "permission denied for schema public"
Verifica que el usuario de PostgreSQL tiene permisos

### Error: "Connection refused" en Redis
Asegúrate que Redis está corriendo: `redis-cli ping`

### Error: CORS
Verifica que tu dominio está en `CORS_ALLOWED_ORIGINS` en settings.py

---

## Siguiente Paso: Desarrollo Frontend

El CRM está listo para conectar con un frontend en React/Vue. Los endpoints están documentados en `/api/schema/`

Ejemplo de conexión desde frontend:

```javascript
const API_URL = 'http://localhost:8000/api/v1';
const token = localStorage.getItem('access_token');

fetch(`${API_URL}/conversations/conversations/?account_id=1`, {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Documentación Completa

Ver `README.md` para documentación completa
Ver `ADVANCED_GUIDE.md` para configuraciones avanzadas
