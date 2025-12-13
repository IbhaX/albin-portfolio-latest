from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ['short_content', 'author', 'post', 'is_approved', 'is_hidden', 'is_deleted', 'created_at']
    list_filter = ['is_approved', 'is_hidden', 'is_deleted', 'created_at']
    search_fields = ['content', 'author__username', 'post__title']
    raw_id_fields = ['post', 'author', 'parent']
    list_editable = ['is_approved', 'is_hidden']
    date_hierarchy = 'created_at'
    
    actions = ['approve_comments', 'hide_comments', 'unhide_comments', 'delete_comments']

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'

    @admin.action(description='Approve selected comments')
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description='Hide selected comments')
    def hide_comments(self, request, queryset):
        queryset.update(is_hidden=True)

    @admin.action(description='Unhide selected comments')
    def unhide_comments(self, request, queryset):
        queryset.update(is_hidden=False)

    @admin.action(description='Soft delete selected comments')
    def delete_comments(self, request, queryset):
        for comment in queryset:
            comment.soft_delete()
