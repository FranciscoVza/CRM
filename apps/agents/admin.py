from django.contrib import admin
from .models import Agent, AgentSkill, AgentShift, AgentStatistics


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['account', 'availability', 'current_conversations', 'max_conversations', 'created_at']
    search_fields = ['account__user__email']
    list_filter = ['availability', 'created_at']


@admin.register(AgentSkill)
class AgentSkillAdmin(admin.ModelAdmin):
    list_display = ['agent', 'name', 'level', 'created_at']
    search_fields = ['name', 'agent__account__user__email']
    list_filter = ['level', 'created_at']


@admin.register(AgentShift)
class AgentShiftAdmin(admin.ModelAdmin):
    list_display = ['agent', 'day_of_week', 'start_time', 'end_time', 'created_at']
    search_fields = ['agent__account__user__email']
    list_filter = ['day_of_week', 'created_at']


@admin.register(AgentStatistics)
class AgentStatisticsAdmin(admin.ModelAdmin):
    list_display = ['agent', 'conversations_handled', 'customer_satisfaction_score', 'updated_at']
    search_fields = ['agent__account__user__email']
    list_filter = ['updated_at']
