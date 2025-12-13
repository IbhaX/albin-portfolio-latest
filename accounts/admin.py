from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'role', 'is_member', 'is_banned', 'is_active', 'date_joined']
    list_filter = ['role', 'is_member', 'is_banned', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Membership & Role', {
            'fields': ('is_member', 'role', 'bio', 'avatar', 'website')
        }),
        ('Moderation', {
            'fields': ('is_banned', 'ban_reason')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Membership & Role', {
            'fields': ('is_member', 'role')
        }),
    )
    
    actions = ['make_member', 'revoke_membership', 'make_moderator', 'ban_user', 'unban_user']

    @admin.action(description='Grant membership to selected users')
    def make_member(self, request, queryset):
        queryset.update(is_member=True)

    @admin.action(description='Revoke membership from selected users')
    def revoke_membership(self, request, queryset):
        queryset.update(is_member=False)

    @admin.action(description='Make selected users moderators')
    def make_moderator(self, request, queryset):
        queryset.update(role='staff', is_member=True)

    @admin.action(description='Ban selected users from commenting')
    def ban_user(self, request, queryset):
        queryset.update(is_banned=True)

    @admin.action(description='Unban selected users')
    def unban_user(self, request, queryset):
        queryset.update(is_banned=False, ban_reason='')
