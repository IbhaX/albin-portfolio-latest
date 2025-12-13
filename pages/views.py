from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import (
    SiteSettings, LandingSection, Skill, Experience,
    Education, Workshop, Language
)
from .forms import ContactForm
from portfolio.models import PersonalProject


def home(request):
    """IBHAX company landing page - freelance services."""
    settings = SiteSettings.load()
    
    # Group skills by category for tech stack display
    skills_qs = Skill.objects.all()
    skills_by_category = {}
    for skill in skills_qs:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill.name)
    
    # Get company projects for portfolio preview
    from portfolio.models import CompanyProject
    company_projects = CompanyProject.objects.filter(is_active=True, is_featured=True)[:6]
    
    context = {
        'settings': settings,
        'skills': skills_by_category,
        'company_projects': company_projects,
        'contact_form': ContactForm(),
    }
    return render(request, 'pages/home.html', context)


def personal_portfolio(request):
    """Personal portfolio page matching the original index.html design."""
    settings = SiteSettings.load()
    
    # Group skills by category
    skills_qs = Skill.objects.all()
    skills_by_category = {}
    for skill in skills_qs:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill.name)
    
    # Get personal projects
    projects = PersonalProject.objects.filter(is_active=True)
    
    context = {
        'settings': settings,
        'skills': skills_by_category,
        'experiences': Experience.objects.filter(is_active=True),
        'projects': projects,
        'education': Education.objects.all(),
        'workshops': Workshop.objects.all(),
        'languages': Language.objects.all(),
        'contact_form': ContactForm(),
    }
    return render(request, 'pages/personal_portfolio.html', context)


def contact(request):
    """Contact form submission."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Thank you for your message!'})
            messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
            return redirect('pages:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {'form': form})


@require_POST
def contact_submit(request):
    """HTMX contact form submission."""
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request, 'pages/partials/contact_success.html')
    return render(request, 'pages/partials/contact_form.html', {'form': form})
