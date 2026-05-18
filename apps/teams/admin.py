from django.contrib import admin
from .models import Team, TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'created_at']
    search_fields = ['name']
    list_filter = ['account', 'created_at']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'team', 'role', 'joined_at']
    search_fields = ['user__email', 'team__name']
    list_filter = ['role', 'team', 'joined_at']
