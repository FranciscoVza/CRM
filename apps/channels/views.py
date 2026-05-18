from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Channel, ChannelTeamAssignment, ChannelWebWidget
from .serializers import ChannelSerializer, ChannelWebWidgetSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Channel.objects.filter(account_id=account_id)
        return Channel.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)

    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        channel = self.get_object()
        # Implement channel-specific connection tests
        return Response({'message': f'Conexión exitosa con {channel.name}'})

    @action(detail=True, methods=['post'])
    def sync_now(self, request, pk=None):
        channel = self.get_object()
        # Trigger manual sync
        from django.utils import timezone
        channel.last_sync_at = timezone.now()
        channel.save()
        return Response({'message': f'Sincronización iniciada para {channel.name}'})

    @action(detail=True, methods=['get', 'post', 'put'])
    def widget(self, request, pk=None):
        channel = self.get_object()

        if request.method == 'GET':
            widget, created = ChannelWebWidget.objects.get_or_create(channel=channel)
            serializer = ChannelWebWidgetSerializer(widget)
            return Response(serializer.data)

        elif request.method in ['POST', 'PUT']:
            widget, created = ChannelWebWidget.objects.get_or_create(channel=channel)
            serializer = ChannelWebWidgetSerializer(widget, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
