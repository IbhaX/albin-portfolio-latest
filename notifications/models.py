from django.db import models
from django.conf import settings


class Notification(models.Model):
    """User notifications for various events."""
    
    NOTIFICATION_TYPES = [
        ('post_published', 'Your post was published'),
        ('post_rejected', 'Your post was rejected'),
        ('new_comment', 'New comment on your post'),
        ('comment_reply', 'Reply to your comment'),
        ('comment_approved', 'Your comment was approved'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    
    # Related objects
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.recipient.username}: {self.title}"
    
    def get_url(self):
        """Get the URL to navigate to when clicking the notification."""
        if self.post:
            if self.comment:
                return f"{self.post.get_absolute_url()}#comment-{self.comment.id}"
            return self.post.get_absolute_url()
        return '/'
    
    @classmethod
    def create_post_published(cls, post):
        """Create notification when a post is published."""
        return cls.objects.create(
            recipient=post.author,
            notification_type='post_published',
            title='Your post has been published!',
            message=f'"{post.title}" is now live and visible to everyone.',
            post=post
        )
    
    @classmethod
    def create_post_rejected(cls, post, reason=''):
        """Create notification when a post is rejected."""
        msg = f'"{post.title}" was not approved.'
        if reason:
            msg += f' Reason: {reason}'
        return cls.objects.create(
            recipient=post.author,
            notification_type='post_rejected',
            title='Your post needs revision',
            message=msg,
            post=post
        )
    
    @classmethod
    def create_new_comment(cls, comment):
        """Create notification when someone comments on your post."""
        if comment.author == comment.post.author:
            return None  # Don't notify yourself
        return cls.objects.create(
            recipient=comment.post.author,
            sender=comment.author,
            notification_type='new_comment',
            title=f'{comment.author.username} commented on your post',
            message=comment.content[:100] + ('...' if len(comment.content) > 100 else ''),
            post=comment.post,
            comment=comment
        )
    
    @classmethod
    def create_comment_reply(cls, reply):
        """Create notification when someone replies to your comment."""
        if not reply.parent:
            return None
        if reply.author == reply.parent.author:
            return None  # Don't notify yourself
        return cls.objects.create(
            recipient=reply.parent.author,
            sender=reply.author,
            notification_type='comment_reply',
            title=f'{reply.author.username} replied to your comment',
            message=reply.content[:100] + ('...' if len(reply.content) > 100 else ''),
            post=reply.post,
            comment=reply
        )
