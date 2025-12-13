from django.db import models
from django.urls import reverse
from django.conf import settings
from slugify import slugify


class Category(models.Model):
    """Blog post categories."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Blog post tags."""
    
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog posts with SEO-friendly URLs."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    featured_image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    excerpt = models.TextField(blank=True, help_text='Short description for previews')
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True, help_text='SEO meta description')
    meta_keywords = models.CharField(max_length=255, blank=True, help_text='Comma-separated keywords')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    allow_comments = models.BooleanField(default=True)
    comments_locked = models.BooleanField(default=False, help_text='Lock thread from new comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    @property
    def comment_count(self):
        return self.comments.filter(is_approved=True).count()

    @property
    def is_pending(self):
        return self.status == 'pending'

    @property
    def is_published(self):
        return self.status == 'published'

    def can_edit(self, user):
        """Check if user can edit this post."""
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return self.author == user and self.status in ['draft', 'pending', 'rejected']

    def can_delete(self, user):
        """Check if user can delete this post."""
        if not user.is_authenticated:
            return False
        if user.is_superuser or user.is_staff:
            return True
        return self.author == user and self.status != 'published'
