from django.db import models
from django.conf import settings


class ModerationLog(models.Model):
    """Log of moderation actions for audit trail."""
    
    ACTION_CHOICES = [
        ('approve_comment', 'Approved Comment'),
        ('hide_comment', 'Hid Comment'),
        ('delete_comment', 'Deleted Comment'),
        ('approve_post', 'Approved Post'),
        ('reject_post', 'Rejected Post'),
        ('ban_user', 'Banned User'),
        ('unban_user', 'Unbanned User'),
        ('lock_thread', 'Locked Thread'),
        ('unlock_thread', 'Unlocked Thread'),
        ('restrict_user', 'Restricted User'),
    ]
    
    moderator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moderation_actions'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='moderation_received'
    )
    target_comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    target_post = models.ForeignKey(
        'blog.Post',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Moderation Log'
        verbose_name_plural = 'Moderation Logs'

    def __str__(self):
        return f"{self.moderator.username} - {self.get_action_display()} - {self.created_at}"


class UserRestriction(models.Model):
    """Temporary or permanent restrictions on users."""
    
    RESTRICTION_TYPES = [
        ('comment_ban', 'Cannot Comment'),
        ('temporary_ban', 'Temporary Ban'),
        ('permanent_ban', 'Permanent Ban'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='restrictions'
    )
    restriction_type = models.CharField(max_length=20, choices=RESTRICTION_TYPES)
    reason = models.TextField()
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='issued_restrictions'
    )
    starts_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True, help_text='Leave blank for permanent')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-starts_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_restriction_type_display()}"
