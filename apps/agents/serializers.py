from rest_framework import serializers
from .models import Agent, AgentSkill, AgentShift, AgentStatistics


class AgentSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentSkill
        fields = ['id', 'name', 'level', 'created_at']
        read_only_fields = ['id', 'created_at']


class AgentShiftSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField()

    class Meta:
        model = AgentShift
        fields = ['id', 'day_of_week', 'day_name', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_day_name(self, obj):
        days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return days[obj.day_of_week]


class AgentStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentStatistics
        fields = ['conversations_handled', 'average_resolution_time', 'customer_satisfaction_score',
                  'messages_sent', 'updated_at']
        read_only_fields = ['updated_at']


class AgentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='account.user.email', read_only=True)
    user_name = serializers.SerializerMethodField()
    account_name = serializers.CharField(source='account.account.name', read_only=True)
    skills = AgentSkillSerializer(many=True, read_only=True)
    shifts = AgentShiftSerializer(many=True, read_only=True)
    statistics = AgentStatisticsSerializer(read_only=True)

    class Meta:
        model = Agent
        fields = ['id', 'user_email', 'user_name', 'account_name', 'availability', 'auto_assignment',
                  'max_conversations', 'current_conversations', 'total_conversations',
                  'resolved_conversations', 'average_response_time', 'skills', 'shifts',
                  'statistics', 'created_at', 'updated_at']
        read_only_fields = ['id', 'total_conversations', 'resolved_conversations', 'average_response_time', 'created_at', 'updated_at']

    def get_user_name(self, obj):
        user = obj.account.user
        return f"{user.first_name} {user.last_name}".strip() or user.email
