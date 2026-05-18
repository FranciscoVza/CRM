from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact, ContactLabel, ContactActivity, ContactSegment, ContactLabelAssignment
from .serializers import (
    ContactSerializer, ContactListSerializer, ContactLabelSerializer,
    ContactActivitySerializer, ContactSegmentSerializer
)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'company']
    search_fields = ['name', 'email', 'phone', 'company']
    ordering_fields = ['created_at', 'name', 'last_activity']
    ordering = ['-created_at']

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Contact.objects.filter(account_id=account_id)
        return Contact.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ContactListSerializer
        return ContactSerializer

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)

    @action(detail=True, methods=['post'])
    def add_label(self, request, pk=None):
        contact = self.get_object()
        label_id = request.data.get('label_id')

        try:
            label = ContactLabel.objects.get(id=label_id, account=contact.account)
            assignment, created = ContactLabelAssignment.objects.get_or_create(
                contact=contact,
                label=label
            )
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        except ContactLabel.DoesNotExist:
            return Response({'error': 'Etiqueta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_label(self, request, pk=None):
        contact = self.get_object()
        label_id = request.data.get('label_id')

        try:
            assignment = ContactLabelAssignment.objects.get(
                contact=contact,
                label_id=label_id
            )
            assignment.delete()
            serializer = ContactSerializer(contact)
            return Response(serializer.data)
        except ContactLabelAssignment.DoesNotExist:
            return Response({'error': 'Asignación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def add_activity(self, request, pk=None):
        contact = self.get_object()
        activity = ContactActivity.objects.create(
            contact=contact,
            activity_type=request.data.get('activity_type'),
            title=request.data.get('title'),
            description=request.data.get('description', ''),
            metadata=request.data.get('metadata', {}),
            created_by=request.user.email
        )
        serializer = ContactActivitySerializer(activity)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactLabelViewSet(viewsets.ModelViewSet):
    serializer_class = ContactLabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return ContactLabel.objects.filter(account_id=account_id)
        return ContactLabel.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)


class ContactSegmentViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSegmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return ContactSegment.objects.filter(account_id=account_id)
        return ContactSegment.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)
