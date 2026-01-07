# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from ACCOUNTS.models import User
from HOSTEL.models import RoomAllocation, Fee, DailyTask
from NOTIFICATIONS.models import Notification
from COMPLAINTS.models import Complaint
from HOSTEL.models import EmergencyContact
from .models import Student, Room
from .forms import StudentForm, RoomForm
from django.contrib import messages

def student_dashboard(request):
    user = request.user
    # Get room info
    room_info = RoomAllocation.objects.filter(student=user).first()
    # Get fee info
    fee_info = Fee.objects.filter(student=user).first()
    # Notifications
    notifications = Notification.objects.filter(user=user, read=False)
    # Complaints
    complaints = Complaint.objects.filter(student=user)

    context = {
        'user': user,
        'room_info': room_info,
        'fee_info': fee_info,
        'notifications': notifications,
        'complaints': complaints
    }
    return render(request, 'accounts/dashboard_student.html', context)

def staff_dashboard(request):
    user = request.user
    # Staff tasks
    tasks = DailyTask.objects.filter(staff=user)
    # Complaints assigned (or all pending)
    complaints = Complaint.objects.filter(status='pending')
    # Notifications
    notifications = Notification.objects.filter(user=user, read=False)
    # Emergency contacts
    emergencies = EmergencyContact.objects.all()

    context = {
        'user': user,
        'tasks': tasks,
        'complaints': complaints,
        'notifications': notifications,
        'emergencies': emergencies,
    }
    return render(request, 'accounts/dashboard_staff.html', context)


def add_task(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        DailyTask.objects.create(staff=request.user, task=task_text)
        return redirect('staff_dashboard')
    return render(request, 'hostel/add_task.html')

#  STUDENT CRUD
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                student = form.save()
                messages.success(request, f'Student {student.name} added successfully!')
                return redirect('student_list')
            except Exception as e:
                messages.error(request, f'Error adding student: {str(e)}')
        else:
            # Form has errors, they will be displayed in template
            pass
    else:
        form = StudentForm()
    
    return render(request, 'hostel/add_student.html', {'form': form})

def student_list(request):
    students = Student.objects.all().order_by('-id')  # Newest first
    return render(request, 'hostel/student_list.html', {'students': students})

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Student {student.name} updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    return render(request, 'hostel/edit_student.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student_name = student.name
    student.delete()
    messages.success(request, f'Student {student_name} deleted successfully!')
    return redirect('student_list')


# ROOM CRUD
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/room_list.html', {'rooms': rooms})

def add_room(request):
    form = RoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'hostel/add_room.html', {'form': form})

def edit_room(request, id):
    room = get_object_or_404(Room, id=id)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'hostel/edit_room.html', {'form': form})

def delete_room(request, id):
    room = get_object_or_404(Room, id=id)
    room.delete()
    return redirect('room_list')

def allocate_room(request):
    students = Student.objects.filter(room__isnull=True)  # Only show unallocated students
    rooms = Room.objects.filter(is_occupied=False)  # Only show available rooms
    total_rooms = Room.objects.count()
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        room_id = request.POST.get('room_id')
        
        try:
            student = Student.objects.get(id=student_id)
            room = Room.objects.get(id=room_id)
            
            # Allocate room to student
            student.room = room
            student.save()
            
            # Update room occupancy
            room.is_occupied = True
            room.save()
            
            messages.success(request, f'Room {room.room_number} allocated to {student.name} successfully!')
            return redirect('student_list')
            
        except (Student.DoesNotExist, Room.DoesNotExist) as e:
            messages.error(request, 'Error allocating room. Please try again.')
    
    context = {
        'students': students,
        'rooms': rooms,
        'total_rooms': total_rooms,
    }
    return render(request, 'hostel/allocate_room.html', context)