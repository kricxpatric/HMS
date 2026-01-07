from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Room

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_no', 'name', 'email', 'phone', 'get_room_number']
    list_filter = ['room']  # Only use existing fields
    search_fields = ['roll_no', 'name', 'email']
    
    def get_room_number(self, obj):
        return obj.room.room_number if obj.room else "Not Assigned"
    get_room_number.short_description = 'Room Number'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'floor', 'capacity', 'current_occupancy', 'is_available']
    list_filter = ['floor', 'is_available']
