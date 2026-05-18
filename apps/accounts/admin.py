from django.contrib import admin
from .models import User, Account, AccountUser, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'first_name', 'is_staff', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_active', 'created_at']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'plan', 'active', 'created_at']
    search_fields = ['name', 'slug']
    list_filter = ['plan', 'active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(AccountUser)
class AccountUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'account', 'role', 'joined_at']
    search_fields = ['user__email', 'account__name']
    list_filter = ['role', 'joined_at']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'availability', 'last_seen']
    search_fields = ['user__email']
    list_filter = ['availability']
