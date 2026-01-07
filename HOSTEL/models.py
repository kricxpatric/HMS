from django.db import models

# Create your models here.
from ACCOUNTS.models import User
from django.utils import timezone 
from django.conf import settings

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField(default=1)  # Add this line
    capacity = models.IntegerField(default=1)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Room {self.room_number}"

class Student(models.Model):
    name = models.CharField(max_length=100, default="Unknown Student")
    roll_no = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True, default="default@gmail.com")
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=15, default="0000000000")

class RoomAllocation(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    allocated_on = models.DateField(auto_now_add=True)

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.username} - {'Paid' if self.paid else 'Pending'}"

class DailyTask(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.TextField()
    date = models.DateField(auto_now_add=True)

STATUS_CHOICES = [
    ('active', 'Active'),
    ('resolved', 'Resolved'),
]

class EmergencyContact(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_name = models.CharField(max_length=100, default='Unknown')
    contact_number = models.CharField(max_length=15, default='0000000000')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.contact_name} - {self.student.username}"

