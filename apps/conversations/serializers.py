from rest_framework import serializers
from .models import Conversation, Message, ConversationActivity, ConversationNote, ConversationLabel


class MessageSerializer(serializers.ModelSerializer):
    sender_display_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_display_name', 'sender_name', 'message_type', 'content',
                  'attachments', 'sent_at', 'read_at', 'external_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_sender_display_name(self, obj):
        if obj.sender:
            return f"{obj.sender.first_name} {obj.sender.last_name}".strip() or obj.sender.email
        return obj.sender_name


class ConversationActivitySerializer(serializers.ModelSerializer):
    performed_by_email = serializers.EmailField(source='performed_by.email', read_only=True)

    class Meta:
        model = ConversationActivity
        fields = ['id', 'activity_type', 'performed_by', 'performed_by_email', 'description',
                  'metadata', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationNoteSerializer(serializers.ModelSerializer):
    author_email = serializers.EmailField(source='author.email', read_only=True)

    class Meta:
        model = ConversationNote
        fields = ['id', 'author', 'author_email', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConversationLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationLabel
        fields = ['id', 'name', 'color', 'created_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    activities = ConversationActivitySerializer(many=True, read_only=True)
    notes = ConversationNoteSerializer(many=True, read_only=True)
    labels = ConversationLabelSerializer(many=True, read_only=True)
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True, allow_null=True)

    class Meta:
        model = Conversation
        fields = ['id', 'subject', 'description', 'status', 'priority', 'source', 'contact_name',
                  'assignee', 'assignee_email', 'labels', 'messages', 'activities', 'notes',
                  'first_response_at', 'last_message_at', 'resolution_time', 'waiting_since',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'first_response_at', 'last_message_at']


class ConversationListSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.name', read_only=True)
    assignee_email = serializers.EmailField(source='assignee.email', read_only=True, allow_null=True)
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'subject', 'status', 'priority', 'source', 'contact_name',
                  'assignee_email', 'messages_count', 'last_message_at', 'updated_at']
        read_only_fields = ['id', 'updated_at']

    def get_messages_count(self, obj):
        return obj.messages.count()
