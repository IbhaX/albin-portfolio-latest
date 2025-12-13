from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey


class Comment(MPTTModel):
    """
    Threaded comments using MPTT (Modified Preorder Tree Traversal).
    Supports unlimited nesting depth like Reddit-style comments.
    """
    
    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False, help_text='Hidden by moderator')
    is_deleted = models.BooleanField(default=False, help_text='Soft deleted')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited_at = models.DateTimeField(null=True, blank=True)
    
    class MPTTMeta:
        order_insertion_by = ['created_at']

    class Meta:
        ordering = ['tree_id', 'lft']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_display_content(self):
        """Return content or placeholder if deleted/hidden."""
        if self.is_deleted:
            return '[deleted]'
        if self.is_hidden:
            return '[hidden by moderator]'
        return self.content

    def can_edit(self, user):
        """Check if user can edit this comment."""
        if not user.is_authenticated:
            return False
        return self.author == user and not self.is_deleted

    def can_delete(self, user):
        """Check if user can delete this comment."""
        if not user.is_authenticated:
            return False
        return self.author == user or user.can_moderate()

    def can_reply(self, user):
        """Check if user can reply to this comment."""
        if not user.is_authenticated:
            return False
        if not user.can_comment():
            return False
        if self.post.comments_locked:
            return False
        return True

    def soft_delete(self):
        """Soft delete the comment, preserving thread structure."""
        self.is_deleted = True
        self.content = ''
        self.save()

    def get_reply_count(self):
        """Get count of all replies in this thread."""
        return self.get_descendant_count()
