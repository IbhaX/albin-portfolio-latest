from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with membership and role support."""
    
    ROLE_CHOICES = [
        ('member', 'Member'),
        ('staff', 'Staff/Moderator'),
        ('admin', 'Admin'),
    ]
    
    is_member = models.BooleanField(default=False, help_text="Can comment on blog posts")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    is_banned = models.BooleanField(default=False, help_text="Banned from commenting")
    ban_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role in ['staff', 'admin'] or self.is_staff

    @property
    def is_site_admin(self):
        return self.role == 'admin' or self.is_superuser

    def can_comment(self):
        return self.is_member and not self.is_banned and self.is_active

    def can_moderate(self):
        return self.is_moderator and self.is_active
