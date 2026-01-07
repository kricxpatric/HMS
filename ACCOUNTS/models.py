from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff/Warden'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Add related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',  # Changed related_name
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Changed related_name
        related_query_name='user',
    )
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True, blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.roll_no})"
    
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    current_occupancy = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room {self.room_number}"