# manage_groups.py
import os
import django
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS_PROJECT.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def setup_groups():
    """Create the basic groups for the hostel management system"""
    groups = ['students', 'staff', 'admins']
    
    for group_name in groups:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"✓ Created group: {group_name}")
        else:
            print(f"✓ Group already exists: {group_name}")

def list_groups():
    """List all existing groups"""
    groups = Group.objects.all()
    print("\nExisting Groups:")
    for group in groups:
        print(f" - {group.name} ({group.permissions.count()} permissions)")

if __name__ == '__main__':
    print("Setting up groups...")
    setup_groups()
    list_groups()
    print("\nGroup setup completed!")