from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_tinymce_api_key():
    """Return the TinyMCE API key from settings."""
    return getattr(settings, 'TINYMCE_API_KEY', 'no-api-key')
