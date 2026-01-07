from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Room

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role',)}),
    )

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_no', 'name', 'email', 'phone', 'get_room_number']
    list_filter = ['room']
    search_fields = ['roll_no', 'name', 'email']
    
    def get_room_number(self, obj):
        return obj.room.room_number if obj.room else "Not Assigned"
    get_room_number.short_description = 'Room Number'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'capacity', 'is_occupied', 'get_student_count', 'get_occupancy_status']
    list_filter = ['is_occupied', 'capacity']
    search_fields = ['room_number']
    
    def get_student_count(self, obj):
        return obj.student_set.count()
    get_student_count.short_description = 'Current Students'
    
    def get_occupancy_status(self, obj):
        if obj.student_set.count() >= obj.capacity:
            return "Full"
        elif obj.student_set.count() > 0:
            return "Partially Occupied"
        else:
            return "Empty"
    get_occupancy_status.short_description = 'Occupancy Status'


