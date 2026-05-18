from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Agent, AgentSkill, AgentShift
from .serializers import AgentSerializer, AgentSkillSerializer, AgentShiftSerializer


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        account_id = self.request.query_params.get('account_id')
        if account_id:
            return Agent.objects.filter(account__account_id=account_id).select_related('account').prefetch_related('skills', 'shifts', 'statistics')
        return Agent.objects.none()

    @action(detail=True, methods=['post'])
    def change_availability(self, request, pk=None):
        agent = self.get_object()
        new_availability = request.data.get('availability')

        if new_availability not in dict(Agent.AVAILABILITY_CHOICES):
            return Response({'error': 'Disponibilidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

        agent.availability = new_availability
        agent.save()
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_skill(self, request, pk=None):
        agent = self.get_object()
        name = request.data.get('name')
        level = request.data.get('level', 1)

        skill, created = AgentSkill.objects.get_or_create(
            agent=agent,
            name=name,
            defaults={'level': level}
        )

        if not created:
            skill.level = level
            skill.save()

        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def remove_skill(self, request, pk=None):
        agent = self.get_object()
        skill_id = request.data.get('skill_id')

        try:
            skill = AgentSkill.objects.get(id=skill_id, agent=agent)
            skill.delete()
            serializer = AgentSerializer(agent)
            return Response(serializer.data)
        except AgentSkill.DoesNotExist:
            return Response({'error': 'Habilidad no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def add_shift(self, request, pk=None):
        agent = self.get_object()
        day_of_week = request.data.get('day_of_week')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        shift = AgentShift.objects.create(
            agent=agent,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time
        )

        serializer = AgentSerializer(agent)
        return Response(serializer.data)
