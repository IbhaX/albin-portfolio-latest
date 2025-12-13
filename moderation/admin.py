from django.contrib import admin
from .models import ModerationLog, UserRestriction


@admin.register(ModerationLog)
class ModerationLogAdmin(admin.ModelAdmin):
    list_display = ['moderator', 'action', 'target_user', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['moderator__username', 'target_user__username', 'reason']
    raw_id_fields = ['moderator', 'target_user', 'target_comment', 'target_post']
    readonly_fields = ['moderator', 'action', 'target_user', 'target_comment', 'target_post', 'reason', 'created_at']
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(UserRestriction)
class UserRestrictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'restriction_type', 'issued_by', 'starts_at', 'expires_at', 'is_active']
    list_filter = ['restriction_type', 'is_active', 'starts_at']
    search_fields = ['user__username', 'reason']
    raw_id_fields = ['user', 'issued_by']
    list_editable = ['is_active']
