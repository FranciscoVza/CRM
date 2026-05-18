from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer


class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Team.objects.filter(account_id=account_id).prefetch_related('members')
        return Team.objects.none()

    def perform_create(self, serializer):
        account_id = self.request.query_params.get('account_id')
        serializer.save(account_id=account_id)

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')

        try:
            from apps.accounts.models import User
            user = User.objects.get(id=user_id)
            member, created = TeamMember.objects.get_or_create(
                team=team,
                user=user,
                defaults={'role': role}
            )

            if not created:
                member.role = role
                member.save()

            serializer = TeamSerializer(team)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        team = self.get_object()
        user_id = request.data.get('user_id')

        try:
            member = TeamMember.objects.get(team=team, user_id=user_id)
            member.delete()
            serializer = TeamSerializer(team)
            return Response(serializer.data)
        except TeamMember.DoesNotExist:
            return Response({'error': 'Miembro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
