from django.db import models
from django.urls import reverse
from slugify import slugify


class PortfolioCategory(models.Model):
    """Categories for portfolio items."""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = 'Portfolio Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PersonalProject(models.Model):
    """Personal portfolio projects."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='personal_projects'
    )
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    technologies = models.TextField(help_text='Comma-separated list')
    featured_image = models.ImageField(upload_to='portfolio/personal/', blank=True, null=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Personal Project'
        verbose_name_plural = 'Personal Projects'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:personal_detail', kwargs={'slug': self.slug})

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class CompanyProject(models.Model):
    """Company/Client portfolio projects."""
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    company_name = models.CharField(max_length=200)
    category = models.ForeignKey(
        PortfolioCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='company_projects'
    )
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    role = models.CharField(max_length=200, blank=True, help_text='Your role in the project')
    technologies = models.TextField(help_text='Comma-separated list')
    achievements = models.TextField(blank=True, help_text='One achievement per line')
    featured_image = models.ImageField(upload_to='portfolio/company/', blank=True, null=True)
    project_url = models.URLField(blank=True)
    case_study_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_confidential = models.BooleanField(default=False, help_text='Hide sensitive details')
    order = models.PositiveIntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-start_date']
        verbose_name = 'Company Project'
        verbose_name_plural = 'Company Projects'

    def __str__(self):
        return f"{self.title} ({self.company_name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:company_detail', kwargs={'slug': self.slug})

    def get_tech_list(self):
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def get_achievements_list(self):
        return [a.strip() for a in self.achievements.split('\n') if a.strip()]


class ProjectImage(models.Model):
    """Additional images for portfolio projects."""
    
    personal_project = models.ForeignKey(
        PersonalProject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images'
    )
    company_project = models.ForeignKey(
        CompanyProject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images'
    )
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        project = self.personal_project or self.company_project
        return f"Image for {project}"
