from django.contrib import admin
from .models import (
    SiteSettings, LandingSection, Skill, Experience, 
    Education, Workshop, Language, ContactMessage
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Site Info', {
            'fields': ('site_name', 'site_tagline')
        }),
        ('Owner Info', {
            'fields': ('owner_name', 'owner_title', 'owner_summary', 'profile_image', 'resume_file')
        }),
        ('Contact', {
            'fields': ('owner_email', 'owner_phone', 'owner_location')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url', 'twitter_url')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords', 'google_analytics_id')
        }),
    )
    
    class Media:
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'admin/js/tinymce_init.js',
        )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(LandingSection)
class LandingSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'section_type', 'order', 'is_active']
    list_filter = ['section_type', 'is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'content']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_filter = ['category']
    list_editable = ['order']
    search_fields = ['name', 'category']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'duration', 'order', 'is_active']
    list_filter = ['is_active']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'company', 'description']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'year', 'order']
    list_editable = ['order']


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ['title', 'order']
    list_editable = ['order']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'proficiency', 'order']
    list_editable = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'name', 'email', 'created_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read', 'is_replied']
    
    def has_add_permission(self, request):
        return False
