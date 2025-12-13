"""
Script to create a superuser for Django admin.
Run with: python manage.py shell < scripts/create_superuser.py
Or: python manage.py shell -c "exec(open('scripts/create_superuser.py').read())"
"""
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ibhax.settings')

import django
django.setup()

from accounts.models import User

def create_admin():
    username = 'admin'
    email = 'albin.anthony.dev@gmail.com'
    password = 'admin123'  # Change this in production!
    
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists")
        user = User.objects.get(username=username)
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superuser '{username}' created")
    
    # Ensure admin has all permissions
    user.is_member = True
    user.role = 'admin'
    user.save()
    print(f"User '{username}' configured as admin with full permissions")
    print(f"\nLogin credentials:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"\n[WARNING] CHANGE THE PASSWORD IN PRODUCTION!")

if __name__ == '__main__':
    create_admin()
