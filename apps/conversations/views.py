from rest_framework import viewsets, status, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Conversation, Message, ConversationActivity, ConversationNote, ConversationLabel
from .serializers import (
    ConversationSerializer, ConversationListSerializer, MessageSerializer,
    ConversationActivitySerializer, ConversationNoteSerializer, ConversationLabelSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'source', 'assignee']
    search_fields = ['subject', 'description', 'contact__name', 'contact__email']
    ordering_fields = ['created_at', 'last_message_at', 'priority']
    ordering = ['-updated_at']

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Conversation.objects.filter(account_id=account_id).prefetch_related('messages', 'activities', 'notes', 'labels')
        return Conversation.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        conversation = serializer.save(account_id=account_id)
        ConversationActivity.objects.create(
            conversation=conversation,
            activity_type='status_change',
            performed_by=self.request.user,
            description=f'Conversación creada',
            metadata={'status': 'open'}
        )

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get('user_id')

        try:
            from apps.accounts.models import User
            assignee = User.objects.get(id=user_id)
            old_assignee = conversation.assignee
            conversation.assignee = assignee
            conversation.save()

            ConversationActivity.objects.create(
                conversation=conversation,
                activity_type='assigned',
                performed_by=request.user,
                description=f'Asignado a {assignee.email}' if assignee else 'Asignación removida',
                metadata={'old_assignee': old_assignee.email if old_assignee else None, 'new_assignee': assignee.email if assignee else None}
            )

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        conversation = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Conversation.STATUS_CHOICES):
            return Response({'error': 'Estado inválido'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = conversation.status
        conversation.status = new_status
        if new_status == 'resolved':
            conversation.resolution_time = int((timezone.now() - conversation.created_at).total_seconds() / 60)
        conversation.save()

        ConversationActivity.objects.create(
            conversation=conversation,
            activity_type='status_change',
            performed_by=request.user,
            description=f'Estado cambió de {old_status} a {new_status}',
            metadata={'old_status': old_status, 'new_status': new_status}
        )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_priority(self, request, pk=None):
        conversation = self.get_object()
        new_priority = request.data.get('priority')

        if new_priority not in dict(Conversation.PRIORITY_CHOICES):
            return Response({'error': 'Prioridad inválida'}, status=status.HTTP_400_BAD_REQUEST)

        old_priority = conversation.priority
        conversation.priority = new_priority
        conversation.save()

        ConversationActivity.objects.create(
            conversation=conversation,
            activity_type='priority_change',
            performed_by=request.user,
            description=f'Prioridad cambió de {old_priority} a {new_priority}',
            metadata={'old_priority': old_priority, 'new_priority': new_priority}
        )

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_label(self, request, pk=None):
        conversation = self.get_object()
        label_id = request.data.get('label_id')

        try:
            label = ConversationLabel.objects.get(id=label_id, account=conversation.account)
            conversation.labels.add(label)

            ConversationActivity.objects.create(
                conversation=conversation,
                activity_type='label_added',
                performed_by=request.user,
                description=f'Etiqueta "{label.name}" añadida',
                metadata={'label': label.name}
            )

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except ConversationLabel.DoesNotExist:
            return Response({'error': 'Etiqueta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_label(self, request, pk=None):
        conversation = self.get_object()
        label_id = request.data.get('label_id')

        try:
            label = ConversationLabel.objects.get(id=label_id, account=conversation.account)
            conversation.labels.remove(label)

            ConversationActivity.objects.create(
                conversation=conversation,
                activity_type='label_removed',
                performed_by=request.user,
                description=f'Etiqueta "{label.name}" removida',
                metadata={'label': label.name}
            )

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except ConversationLabel.DoesNotExist:
            return Response({'error': 'Etiqueta no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(conversation_id=conversation_id)
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation_id = self.request.query_params.get('conversation_id')
        message = serializer.save(
            conversation_id=conversation_id,
            sender=self.request.user,
            message_type='outgoing',
            sender_name=self.request.user.email,
            sent_at=timezone.now()
        )

        # Update conversation last_message_at
        conversation = message.conversation
        conversation.last_message_at = timezone.now()
        if not conversation.first_response_at and message.sender:
            conversation.first_response_at = timezone.now()
        conversation.save()


class ConversationNoteViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        if conversation_id:
            return ConversationNote.objects.filter(conversation_id=conversation_id)
        return ConversationNote.objects.none()

    def perform_create(self, serializer):
        conversation_id = self.request.query_params.get('conversation_id')
        serializer.save(
            conversation_id=conversation_id,
            author=self.request.user
        )


class ConversationLabelViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationLabelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return ConversationLabel.objects.filter(account_id=account_id)
        return ConversationLabel.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)
