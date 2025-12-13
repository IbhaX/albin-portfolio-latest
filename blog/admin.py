from django.contrib import admin
from django.utils import timezone
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'allow_comments', 'comments_locked', 'published_at', 'views']
    list_filter = ['status', 'category', 'allow_comments', 'comments_locked', 'created_at', 'published_at']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    list_editable = ['status', 'allow_comments', 'comments_locked']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('featured_image', 'excerpt', 'content')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'published_at', 'allow_comments', 'comments_locked')
        }),
    )
    
    class Media:
        js = (
            'https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js',
            'admin/js/tinymce_init.js',
        )
    
    actions = ['publish_posts', 'unpublish_posts', 'lock_comments', 'unlock_comments']

    @admin.action(description='Publish selected posts')
    def publish_posts(self, request, queryset):
        queryset.update(status='published', published_at=timezone.now())

    @admin.action(description='Unpublish selected posts')
    def unpublish_posts(self, request, queryset):
        queryset.update(status='draft')

    @admin.action(description='Lock comments on selected posts')
    def lock_comments(self, request, queryset):
        queryset.update(comments_locked=True)

    @admin.action(description='Unlock comments on selected posts')
    def unlock_comments(self, request, queryset):
        queryset.update(comments_locked=False)
