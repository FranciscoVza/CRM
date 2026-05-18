from rest_framework import serializers
from .models import Channel, ChannelTeamAssignment, ChannelWebWidget


class ChannelWebWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelWebWidget
        fields = ['title', 'welcome_message', 'widget_color', 'position', 'enabled', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class ChannelSerializer(serializers.ModelSerializer):
    widget = ChannelWebWidgetSerializer(read_only=True)

    class Meta:
        model = Channel
        fields = ['id', 'name', 'channel_type', 'is_active', 'external_account_id', 'sync_enabled',
                  'last_sync_at', 'widget', 'created_at', 'updated_at']
        read_only_fields = ['id', 'external_account_id', 'last_sync_at', 'created_at', 'updated_at']
