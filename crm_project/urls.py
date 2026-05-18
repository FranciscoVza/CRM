"""
URL configuration for crm_project project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="CRM API",
        default_version='v1',
        description="API para CRM similar a ChatWoot",
        contact=openapi.Contact(email="support@crm.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Endpoints
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/contacts/', include('apps.contacts.urls')),
    path('api/v1/conversations/', include('apps.conversations.urls')),
    path('api/v1/agents/', include('apps.agents.urls')),
    path('api/v1/teams/', include('apps.teams.urls')),
    path('api/v1/channels/', include('apps.channels.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),

    # Swagger/OpenAPI
    path('api/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
