from django.conf import settings as django_settings
from .models import SiteSettings


def site_settings(request):
    """Make site settings available in all templates."""
    try:
        return {
            'site_settings': SiteSettings.load(),
            'TINYMCE_API_KEY': getattr(django_settings, 'TINYMCE_API_KEY', 'no-api-key'),
        }
    except Exception:
        return {
            'site_settings': None,
            'TINYMCE_API_KEY': getattr(django_settings, 'TINYMCE_API_KEY', 'no-api-key'),
        }
