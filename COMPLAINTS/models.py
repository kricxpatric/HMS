from django.db import models

# Create your models here.
from ACCOUNTS.models import User

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('resolved', 'Resolved'),
]

class Complaint(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'student'})
    title = models.CharField(max_length=100, default="No Title")
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"

class EmergencyContact(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    role = models.CharField(max_length=10) # staff/admin/student

