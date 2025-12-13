from django.contrib import admin
from .models import PortfolioCategory, PersonalProject, CompanyProject, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(PersonalProject)
class PersonalProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['title', 'description', 'technologies']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_active', 'order']
    inlines = [ProjectImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        ('Technical', {
            'fields': ('technologies', 'featured_image')
        }),
        ('Links', {
            'fields': ('project_url', 'github_url', 'demo_url')
        }),
        ('Display', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    class Media:
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'admin/js/tinymce_init.js',
        )


@admin.register(CompanyProject)
class CompanyProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'company_name', 'category', 'is_featured', 'is_active', 'is_confidential', 'order']
    list_filter = ['category', 'is_featured', 'is_active', 'is_confidential']
    search_fields = ['title', 'company_name', 'description', 'technologies']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'is_active', 'is_confidential', 'order']
    inlines = [ProjectImageInline]
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'company_name', 'category', 'role')
        }),
        ('Content', {
            'fields': ('short_description', 'description', 'achievements', 'featured_image')
        }),
        ('Technical', {
            'fields': ('technologies',)
        }),
        ('Links', {
            'fields': ('project_url', 'case_study_url')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Display', {
            'fields': ('is_featured', 'is_active', 'is_confidential', 'order')
        }),
    )
    
    class Media:
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'admin/js/tinymce_init.js',
        )
