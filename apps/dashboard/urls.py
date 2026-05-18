from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DashboardReportViewSet, DashboardStatsViewSet

router = DefaultRouter()
router.register(r'reports', DashboardReportViewSet, basename='report')
router.register(r'stats', DashboardStatsViewSet, basename='stats')

urlpatterns = [
    path('', include(router.urls)),
]
