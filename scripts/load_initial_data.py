"""
Script to load initial data from the existing profile.json into Django models.
Run with: python manage.py shell < scripts/load_initial_data.py
"""
import os
import sys
import json
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibhax.settings')
django.setup()

from pages.models import SiteSettings, Skill, Experience, Education, Workshop, Language
from portfolio.models import PersonalProject, PortfolioCategory

def load_data():
    # Load profile.json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) if '__file__' in dir() else os.getcwd()
    profile_path = os.path.join(base_dir, 'profile.json')
    
    if not os.path.exists(profile_path):
        print("profile.json not found, skipping data load")
        return
    
    with open(profile_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create or update SiteSettings
    settings, created = SiteSettings.objects.get_or_create(pk=1)
    settings.owner_name = data.get('name', 'Albin Anthony')
    settings.owner_title = data.get('title', '')
    settings.owner_summary = data.get('summary', '')
    
    contact = data.get('contact', {})
    settings.owner_email = contact.get('email', '')
    settings.owner_phone = contact.get('phone', '')
    settings.owner_location = contact.get('location', '')
    settings.linkedin_url = f"https://{contact.get('linkedin', '')}" if contact.get('linkedin') else ''
    settings.github_url = f"https://{contact.get('github', '')}" if contact.get('github') else ''
    settings.save()
    print(f"SiteSettings {'created' if created else 'updated'}")
    
    # Load Skills
    skills_data = data.get('skills', {}).get('categories', {})
    Skill.objects.all().delete()
    order = 0
    for category, skill_list in skills_data.items():
        for skill_name in skill_list:
            Skill.objects.create(
                category=category.replace('_', ' ').title(),
                name=skill_name,
                order=order
            )
            order += 1
    print(f"Loaded {order} skills")
    
    # Load Experience
    Experience.objects.all().delete()
    for idx, exp in enumerate(data.get('experience', [])):
        Experience.objects.create(
            title=exp.get('title', ''),
            company=exp.get('company', ''),
            duration=exp.get('duration', ''),
            description='\n'.join(exp.get('description', [])),
            technologies=', '.join(exp.get('tech', [])),
            icon=exp.get('icon', 'briefcase'),
            order=idx,
            is_active=True
        )
    print(f"Loaded {len(data.get('experience', []))} experiences")
    
    # Load Education
    Education.objects.all().delete()
    for idx, edu in enumerate(data.get('education', [])):
        Education.objects.create(
            name=edu.get('name', ''),
            institution=edu.get('institution', ''),
            year=edu.get('year', ''),
            order=idx
        )
    print(f"Loaded {len(data.get('education', []))} education entries")
    
    # Load Workshops
    Workshop.objects.all().delete()
    for idx, workshop in enumerate(data.get('workshops', [])):
        Workshop.objects.create(
            title=workshop,
            order=idx
        )
    print(f"Loaded {len(data.get('workshops', []))} workshops")
    
    # Load Languages
    Language.objects.all().delete()
    for idx, lang in enumerate(data.get('languages', [])):
        Language.objects.create(
            name=lang.get('name', ''),
            proficiency=lang.get('proficiency', ''),
            order=idx
        )
    print(f"Loaded {len(data.get('languages', []))} languages")
    
    # Load Projects as Personal Projects
    category, _ = PortfolioCategory.objects.get_or_create(
        slug='development',
        defaults={'name': 'Development', 'order': 0}
    )
    
    PersonalProject.objects.all().delete()
    for idx, proj in enumerate(data.get('projects', [])):
        PersonalProject.objects.create(
            title=proj.get('name', ''),
            slug=proj.get('name', '').lower().replace(' ', '-')[:50],
            category=category,
            description=proj.get('description', ''),
            technologies=proj.get('tech', ''),
            project_url=proj.get('link', ''),
            github_url=proj.get('link', '') if 'github' in proj.get('link', '').lower() else '',
            is_featured=idx < 3,
            is_active=True,
            order=idx
        )
    print(f"Loaded {len(data.get('projects', []))} projects")
    
    print("\nData load complete!")

if __name__ == '__main__':
    load_data()
