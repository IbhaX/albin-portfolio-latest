from django.db import models


class SiteSettings(models.Model):
    """Singleton model for site-wide settings editable via admin."""
    
    site_name = models.CharField(max_length=100, default='IBHAX')
    site_tagline = models.CharField(max_length=255, default='Senior Python Engineer & AI Developer')
    owner_name = models.CharField(max_length=100, default='Albin Anthony')
    owner_title = models.CharField(max_length=255, default='Senior Python Developer, Backend Specialist, API Integration Expert')
    owner_summary = models.TextField(blank=True)
    owner_email = models.EmailField(default='albin.anthony.dev@gmail.com')
    owner_phone = models.CharField(max_length=20, blank=True)
    owner_location = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    meta_description = models.TextField(blank=True, help_text='SEO meta description')
    meta_keywords = models.TextField(blank=True, help_text='Comma-separated keywords')
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class LandingSection(models.Model):
    """Editable sections for the landing page."""
    
    SECTION_TYPES = [
        ('hero', 'Hero Section'),
        ('about', 'About Section'),
        ('skills', 'Skills Section'),
        ('experience', 'Experience Section'),
        ('projects', 'Projects Section'),
        ('education', 'Education Section'),
        ('contact', 'Contact Section'),
        ('custom', 'Custom Section'),
    ]
    
    section_type = models.CharField(max_length=20, choices=SECTION_TYPES)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=500, blank=True)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    css_class = models.CharField(max_length=200, blank=True, help_text='Additional CSS classes')
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Landing Section'
        verbose_name_plural = 'Landing Sections'

    def __str__(self):
        return f"{self.get_section_type_display()} - {self.title}"


class Skill(models.Model):
    """Skills grouped by category."""
    
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.category}: {self.name}"


class Experience(models.Model):
    """Work experience entries."""
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    description = models.TextField(help_text='One point per line')
    technologies = models.TextField(blank=True, help_text='Comma-separated')
    icon = models.CharField(max_length=50, default='briefcase')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return f"{self.title} at {self.company}"

    def get_description_list(self):
        return [line.strip() for line in self.description.split('\n') if line.strip()]

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class Education(models.Model):
    """Education entries."""
    
    name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Education'

    def __str__(self):
        return f"{self.name} - {self.institution}"


class Workshop(models.Model):
    """Workshops and training."""
    
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Language(models.Model):
    """Language proficiency."""
    
    name = models.CharField(max_length=50)
    proficiency = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} - {self.proficiency}"


class ContactMessage(models.Model):
    """Contact form submissions."""
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_replied = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} from {self.name}"
