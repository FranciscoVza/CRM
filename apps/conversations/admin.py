from django.contrib import admin
from .models import Conversation, Message, ConversationActivity, ConversationNote, ConversationLabel


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['subject', 'contact', 'account', 'status', 'priority', 'assignee', 'created_at']
    search_fields = ['subject', 'contact__name', 'contact__email']
    list_filter = ['status', 'priority', 'source', 'account', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'conversation', 'message_type', 'created_at']
    search_fields = ['content', 'sender_name']
    list_filter = ['message_type', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(ConversationActivity)
class ConversationActivityAdmin(admin.ModelAdmin):
    list_display = ['activity_type', 'conversation', 'performed_by', 'created_at']
    search_fields = ['description']
    list_filter = ['activity_type', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(ConversationNote)
class ConversationNoteAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'author', 'created_at']
    search_fields = ['content']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ConversationLabel)
class ConversationLabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'color', 'created_at']
    search_fields = ['name']
    list_filter = ['account', 'created_at']
