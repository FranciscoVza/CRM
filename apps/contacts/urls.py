from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, ContactLabelViewSet, ContactSegmentViewSet

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'labels', ContactLabelViewSet, basename='contact-label')
router.register(r'segments', ContactSegmentViewSet, basename='contact-segment')

urlpatterns = [
    path('', include(router.urls)),
]
