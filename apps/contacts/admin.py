from django.contrib import admin
from .models import Contact, ContactLabel, ContactActivity, ContactSegment, ContactLabelAssignment


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'account', 'status', 'company', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company']
    list_filter = ['status', 'account', 'created_at']


@admin.register(ContactLabel)
class ContactLabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'color', 'created_at']
    search_fields = ['name']
    list_filter = ['account', 'created_at']


@admin.register(ContactActivity)
class ContactActivityAdmin(admin.ModelAdmin):
    list_display = ['title', 'contact', 'activity_type', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['activity_type', 'created_at']


@admin.register(ContactSegment)
class ContactSegmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'account', 'created_at']
    search_fields = ['name']
    list_filter = ['account', 'created_at']
