from django.contrib import admin
from .models import Channel, ChannelTeamAssignment, ChannelWebWidget


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['name', 'channel_type', 'account', 'is_active', 'last_sync_at', 'created_at']
    search_fields = ['name']
    list_filter = ['channel_type', 'is_active', 'account', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(ChannelTeamAssignment)
class ChannelTeamAssignmentAdmin(admin.ModelAdmin):
    list_display = ['channel', 'team']
    search_fields = ['channel__name', 'team__name']


@admin.register(ChannelWebWidget)
class ChannelWebWidgetAdmin(admin.ModelAdmin):
    list_display = ['channel', 'enabled', 'widget_color', 'position', 'created_at']
    list_filter = ['enabled', 'position', 'created_at']
