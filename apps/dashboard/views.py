from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import DashboardReport, DashboardMetric
from .serializers import DashboardReportSerializer, DashboardMetricSerializer
from apps.conversations.models import Conversation, Message
from apps.contacts.models import Contact
from apps.agents.models import Agent


class DashboardReportViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return DashboardReport.objects.filter(account_id=account_id)
        return DashboardReport.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)


class DashboardStatsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get overall account statistics"""
        account_id = request.query_params.get('account_id')
        if not account_id:
            return Response({'error': 'account_id required'}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()
        last_7_days = today - timedelta(days=7)

        stats = {
            'conversations': {
                'total': Conversation.objects.filter(account_id=account_id).count(),
                'open': Conversation.objects.filter(account_id=account_id, status='open').count(),
                'resolved': Conversation.objects.filter(account_id=account_id, status='resolved').count(),
                'waiting': Conversation.objects.filter(account_id=account_id, status='waiting').count(),
                'today': Conversation.objects.filter(account_id=account_id, created_at__date=today).count(),
            },
            'contacts': {
                'total': Contact.objects.filter(account_id=account_id).count(),
                'active': Contact.objects.filter(account_id=account_id, status='active').count(),
                'inactive': Contact.objects.filter(account_id=account_id, status='inactive').count(),
            },
            'messages': {
                'total': Message.objects.filter(conversation__account_id=account_id).count(),
                'today': Message.objects.filter(conversation__account_id=account_id, created_at__date=today).count(),
            },
            'agents': {
                'total': Agent.objects.filter(account__account_id=account_id).count(),
                'online': Agent.objects.filter(account__account_id=account_id, availability='online').count(),
            },
        }

        return Response(stats)

    @action(detail=False, methods=['get'])
    def conversation_metrics(self, request):
        """Get conversation metrics"""
        account_id = request.query_params.get('account_id')
        days = int(request.query_params.get('days', 7))

        if not account_id:
            return Response({'error': 'account_id required'}, status=status.HTTP_400_BAD_REQUEST)

        start_date = timezone.now() - timedelta(days=days)

        conversations = Conversation.objects.filter(
            account_id=account_id,
            created_at__gte=start_date
        ).values('status').annotate(count=Count('id')).order_by('status')

        avg_resolution_time = Conversation.objects.filter(
            account_id=account_id,
            status='resolved',
            created_at__gte=start_date,
            resolution_time__isnull=False
        ).values_list('resolution_time', flat=True).average() if hasattr(Conversation.objects.filter(
            account_id=account_id,
            status='resolved',
            created_at__gte=start_date,
            resolution_time__isnull=False
        ).values_list('resolution_time', flat=True), 'average') else 0

        return Response({
            'by_status': list(conversations),
            'average_resolution_time': avg_resolution_time,
        })

    @action(detail=False, methods=['get'])
    def agent_performance(self, request):
        """Get agent performance metrics"""
        account_id = request.query_params.get('account_id')

        if not account_id:
            return Response({'error': 'account_id required'}, status=status.HTTP_400_BAD_REQUEST)

        agents = Agent.objects.filter(
            account__account_id=account_id
        ).values(
            'account__user__email',
            'total_conversations',
            'resolved_conversations',
            'current_conversations',
            'average_response_time'
        )

        return Response(list(agents))

    @action(detail=False, methods=['get'])
    def channel_breakdown(self, request):
        """Get conversation breakdown by channel"""
        account_id = request.query_params.get('account_id')

        if not account_id:
            return Response({'error': 'account_id required'}, status=status.HTTP_400_BAD_REQUEST)

        channels = Conversation.objects.filter(
            account_id=account_id
        ).values('source').annotate(count=Count('id')).order_by('-count')

        return Response(list(channels))
