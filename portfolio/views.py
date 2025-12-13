from django.shortcuts import render, get_object_or_404
from .models import PortfolioCategory, PersonalProject, CompanyProject


def portfolio_home(request):
    """Portfolio landing page showing featured projects."""
    personal_featured = PersonalProject.objects.filter(is_active=True, is_featured=True)[:3]
    company_featured = CompanyProject.objects.filter(is_active=True, is_featured=True)[:3]
    categories = PortfolioCategory.objects.all()
    
    context = {
        'personal_featured': personal_featured,
        'company_featured': company_featured,
        'categories': categories,
    }
    return render(request, 'portfolio/home.html', context)


def personal_list(request):
    """List all personal projects."""
    projects = PersonalProject.objects.filter(is_active=True)
    categories = PortfolioCategory.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'portfolio/personal_list.html', context)


def personal_detail(request, slug):
    """Detail view for a personal project."""
    project = get_object_or_404(PersonalProject, slug=slug, is_active=True)
    related = PersonalProject.objects.filter(
        is_active=True, category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related,
    }
    return render(request, 'portfolio/personal_detail.html', context)


def company_list(request):
    """List all company projects."""
    projects = CompanyProject.objects.filter(is_active=True)
    categories = PortfolioCategory.objects.all()
    
    category_slug = request.GET.get('category')
    if category_slug:
        projects = projects.filter(category__slug=category_slug)
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'portfolio/company_list.html', context)


def company_detail(request, slug):
    """Detail view for a company project."""
    project = get_object_or_404(CompanyProject, slug=slug, is_active=True)
    related = CompanyProject.objects.filter(
        is_active=True, category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related,
    }
    return render(request, 'portfolio/company_detail.html', context)
