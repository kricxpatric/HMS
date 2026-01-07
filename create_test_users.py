# create_test_users.py
import os
import django
import sys

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HMS_PROJECT.settings')
django.setup()

from django.contrib.auth.models import Group
from ACCOUNTS.models import User

def create_test_users():
    """Create test users for each role"""
    
    # Get or create groups
    student_group, _ = Group.objects.get_or_create(name='students')
    staff_group, _ = Group.objects.get_or_create(name='staff')
    admin_group, _ = Group.objects.get_or_create(name='admins')
    
    # Test Student
    student, created = User.objects.get_or_create(
        username='teststudent',
        defaults={
            'email': 'student@test.com',
            'first_name': 'Test',
            'last_name': 'Student'
        }
    )
    if created:
        student.set_password('test123')
        student.groups.add(student_group)
        student.save()
        print("✓ Test student created - Username: teststudent, Password: test123")
    else:
        print("✓ Test student already exists")
    
    # Test Staff
    staff, created = User.objects.get_or_create(
        username='teststaff',
        defaults={
            'email': 'staff@test.com',
            'first_name': 'Test', 
            'last_name': 'Staff'
        }
    )
    if created:
        staff.set_password('test123')
        staff.groups.add(staff_group)
        staff.save()
        print("✓ Test staff created - Username: teststaff, Password: test123")
    else:
        print("✓ Test staff already exists")
    
    # Test Admin
    admin, created = User.objects.get_or_create(
        username='testadmin',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Test',
            'last_name': 'Admin'
        }
    )
    if created:
        admin.set_password('test123')
        admin.groups.add(admin_group)
        admin.save()
        print("✓ Test admin created - Username: testadmin, Password: test123")
    else:
        print("✓ Test admin already exists")

def list_users():
    """List all users and their groups"""
    users = User.objects.all()
    print("\nExisting Users:")
    for user in users:
        groups = ", ".join([group.name for group in user.groups.all()])
        print(f" - {user.username} ({user.email}) - Groups: {groups}")

if __name__ == '__main__':
    print("Creating test users...")
    create_test_users()
    list_users()
    print("\nUser creation completed!")