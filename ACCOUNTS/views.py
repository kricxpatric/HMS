# Create your views here.
from django.db.models import Sum, Count
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from HOSTEL.models import RoomAllocation, Fee, Room, DailyTask, EmergencyContact, Student, User
from ACCOUNTS.models import User              # import models from your apps
from NOTIFICATIONS.models import Notification
from COMPLAINTS.models import Complaint
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Helper functions to check groups
def is_student(user):
    return user.groups.filter(name='students').exists()

def is_staff(user):
    return user.groups.filter(name='staff').exists()

def is_admin(user):
    return user.groups.filter(name='admins').exists()

# Student Dashboard
@login_required
@user_passes_test(is_student, login_url='login_view')
def student_dashboard(request):
    user = request.user
    try:
        room_info = RoomAllocation.objects.filter(student_id=user.id).first()
        fee_info = Fee.objects.filter(student_id=user.id).first()
        notifications = Notification.objects.filter(user_id=user.id, read=False)
        complaints = Complaint.objects.filter(student_id=user.id)

        context = {
            'user': user,
            'room_info': room_info,
            'fee_info': fee_info,
            'notifications': notifications,
            'complaints': complaints
        }
        return render(request, 'accounts/dashboard_student.html', context)
    
    except Exception as e:
        messages.error(request, f'Error loading dashboard: {str(e)}')
        return redirect('home')

# Admin Dashboard
@login_required
def admin_dashboard(request):
    try:
        # Get all users
        all_users = User.objects.all()
        total_users = all_users.count()
        
        # Count students, staff, and admins using your custom role field
        total_students = User.objects.filter(role='student').count()
        total_staff = User.objects.filter(role='staff').count() 
        total_admins = User.objects.filter(role='admin').count()
        
        # Calculate fees collected
        total_fees_collected = Fee.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
        
        # Get complaints data - using 'status' field instead of 'resolved'
        try:
            pending_complaints = Complaint.objects.filter(status='pending').count()
            total_complaints = Complaint.objects.count()
        except Exception as e:
            print(f"Complaints error: {e}")
            pending_complaints = 0
            total_complaints = 0
        
        # Get rooms data
        try:
            total_rooms = Room.objects.count()
        except:
            total_rooms = 0
        
        # Get recent students for the table
        recent_students = User.objects.all().order_by('-date_joined')[:5]
        
        context = {
            'total_students': total_students,
            'total_staff': total_staff,
            'total_admins': total_admins,
            'total_users': total_users,
            'total_fees_collected': total_fees_collected,
            'pending_complaints': pending_complaints,
            'total_complaints': total_complaints,
            'total_rooms': total_rooms,
            'students': recent_students,
        }
        
        return render(request, 'accounts/dashboard_admin.html', context)
        
    except Exception as e:
        # Handle any exceptions and still return a response
        print(f"Error in admin_dashboard: {str(e)}")
        error_context = {
            'total_students': 0,
            'total_staff': 0,
            'total_admins': 0,
            'total_users': 0,
            'total_fees_collected': 0,
            'pending_complaints': 0,
            'total_complaints': 0,
            'total_rooms': 0,
            'students': [],
        }
        return render(request, 'accounts/dashboard_admin.html', error_context)

# Staff Dashboard
@login_required  
@user_passes_test(is_staff, login_url='login_view')
def staff_dashboard(request):
    return render(request, 'accounts/dashboard_staff.html')

def home(request):
    return render(request, 'accounts/home.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        if hasattr(request.user, 'role'):
            if request.user.role == 'admin':
                return redirect('admin_dashboard')
            elif request.user.role == 'staff':
                return redirect('staff_dashboard')
            elif request.user.role == 'student':
                return redirect('student_dashboard')
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Debug: Print user role to console
            print(f"User: {user.username}, Role: {getattr(user, 'role', 'No role')}")
            
            # Redirect based on user role
            if hasattr(user, 'role'):
                if user.role == 'student':
                    return redirect('student_dashboard')
                elif user.role == 'staff':
                    return redirect('staff_dashboard')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
            
            # Default redirect for users without role or superusers
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')  # Redirect to home page

# Signup Views
def signup_view(request):
    return render(request, 'accounts/signup_choice.html')

def student_signup(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_no = request.POST.get('student_id')  # This maps to roll_no 
        phone = request.POST.get('phone')

        # Validate passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return render(request, 'accounts/student_signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'accounts/student_signup.html')

        # Check if email already exists in User model
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'accounts/student_signup.html')

        # Check if roll_no already exists in Student model - CORRECTED
        if Student.objects.filter(roll_no=roll_no).exists():
            messages.error(request, "Student ID already exists!")
            return render(request, 'accounts/student_signup.html')

        # Check if email already exists in Student model
        if Student.objects.filter(email=email).exists():
            messages.error(request, "Email already registered as student!")
            return render(request, 'accounts/student_signup.html')

        try:
            # Create User with student role
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )

            # Create Student profile
            student = Student.objects.create(
                roll_no=roll_no,
                name=f"{first_name} {last_name}",
                email=email,
                phone=phone,
            )

            messages.success(request, "Student account created successfully! You can now login.")
            return redirect('login')

        except Exception as e:
            # If any error occurs, delete the user if created
            if User.objects.filter(username=username).exists():
                User.objects.get(username=username).delete()
            # Delete student if created but user failed
            if Student.objects.filter(roll_no=roll_no).exists():
                Student.objects.get(roll_no=roll_no).delete()
                
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'accounts/student_signup.html')

    return render(request, 'accounts/student_signup.html')

def staff_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        staff_id = request.POST.get('staff_id')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'accounts/staff_signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/staff_signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return render(request, 'accounts/staff_signup.html')
        
        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                role='staff'
            )
            
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome {first_name}! Your staff account has been created successfully.')
            return redirect('staff_dashboard')
            
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
    
    return render(request, 'accounts/staff_signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# Admin can allocate room to a student
def allocate_room(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        room_id = request.POST.get('room_id')
        student = User.objects.get(id=student_id)
        room = Room.objects.get(id=room_id)

        # Check room capacity
        if room.occupied < room.capacity:
            RoomAllocation.objects.create(student=student, room=room)
            room.occupied += 1
            room.save()
            return redirect('admin_dashboard')
        else:
            # room full
            return render(request, 'hostel/allocate_room.html', {'error': 'Room is full', 'students': User.objects.filter(role="student"), 'rooms': Room.objects.all()})
    students = User.objects.filter(role="student")
    rooms = Room.objects.all()
    return render(request, 'hostel/allocate_room.html', {'students': students, 'rooms': rooms})

# Admin - View all fees
def fees_dashboard(request):
    # Total fees collected
    total_fees_collected = Fee.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Total pending fees
    total_fees_pending = Fee.objects.filter(paid=False).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Optional: list of all fees with status
    fees_list = Fee.objects.select_related('student').all()
    
    context = {
        'total_fees_collected': total_fees_collected,
        'total_fees_pending': total_fees_pending,
        'fees_list': fees_list,
    }
    return render(request, 'accounts/fees_dashboard.html', context)

# Admin - Mark fee as paid
def mark_fee_paid(request, fee_id):
    fee = Fee.objects.get(id=fee_id)
    fee.paid = True
    fee.date_paid = timezone.now()
    fee.save()
    return redirect('fees_dashboard')

# Admin/Staff view all complaints
def all_complaints(request):
    complaints = Complaint.objects.all()
    return render(request, 'accounts/all_complaints.html', {'complaints': complaints})

# Mark complaint as resolved
def resolve_complaint(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    complaint.status = 'resolved'
    complaint.save()
    return redirect('all_complaints')

# Reports
def dashboard_reports(request):
    # Total fees collected
    total_fees_collected = Fee.objects.filter(paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

    # Total fees pending
    total_fees_pending = Fee.objects.filter(paid=False).aggregate(Sum('amount'))['amount__sum'] or 0

    # Total students
    total_students = Student.objects.count()

    # Total fees entries
    total_fees_entries = Fee.objects.count()

    context = {
        'total_fees_collected': total_fees_collected,
        'total_fees_pending': total_fees_pending,
        'total_students': total_students,
        'total_fees_entries': total_fees_entries,
    }

    return render(request, 'accounts/dashboard_reports.html', context)

# Student - view their own fees
def student_fees(request):
    fees = Fee.objects.filter(student=request.user)
    return render(request, 'accounts/student_fees.html', {'fees': fees})

# Student submit complaint
def submit_complaint(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Complaint.objects.create(
            student=request.user, 
            title=title, 
            description=description,
            status='pending'
        )
        return redirect('student_complaints')
    return render(request, 'accounts/submit_complaint.html')

# View Student Complaints
def student_complaints(request):
    complaints = Complaint.objects.filter(student=request.user)
    return render(request, 'accounts/student_complaints.html', {'complaints': complaints})

# Student triggers emergency
def trigger_emergency(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        EmergencyContact.objects.create(student=request.user, description=description)
        return redirect('student_dashboard')
    return render(request, 'accounts/trigger_emergency.html')

def add_task(request):
    if request.method == 'POST':
        task_text = request.POST.get('task')
        DailyTask.objects.create(staff=request.user, task=task_text)
        return redirect('staff_dashboard')
    return render(request, 'hostel/add_task.html')

# Send notification
def send_notification(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        message = request.POST.get('message')
        try:
            recipient = User.objects.get(username=recipient_username)
            Notification.objects.create(recipient=recipient, message=message)
        except User.DoesNotExist:
            # handle invalid username
            pass
        return redirect('notifications_dashboard')
    return render(request, 'accounts/send_notification.html')

# View all notifications (for admin/staff)
def notifications_dashboard(request):
    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'accounts/notifications_dashboard.html', {'notifications': notifications})

# For logged-in user
def my_notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'accounts/my_notifications.html', {'notifications': notifications})

# View all emergencies
def view_emergencies(request):
    emergencies = EmergencyContact.objects.all().order_by('-created_at')
    return render(request, 'accounts/view_emergencies.html', {'emergencies': emergencies})

# Resolve an emergency
def resolve_emergency(request, emergency_id):
    emergency = EmergencyContact.objects.get(id=emergency_id)
    emergency.status = 'resolved'
    emergency.save()
    return redirect('view_emergencies')

# Add these role-based login views (AFTER your existing login_view)
def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.role == 'student':
            login(request, user)
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid student credentials')
    return redirect('home')

def staff_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.role == 'staff':
            login(request, user)
            return redirect('staff_dashboard')
        else:
            messages.error(request, 'Invalid staff credentials')
    return redirect('home')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.role == 'admin':
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')
    return redirect('home')

def student_list(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
            else:
                # Create new user with student role
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    role='student'  # Set role as student
                )
                messages.success(request, f'Student {username} created successfully!')
                return redirect('student_list')  # Redirect after success
                
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
    
    # GET request - show only students
    students = User.objects.filter(role='student')  # Filter for students only
    return render(request, 'hostel/student_list.html', {'students': students})

def add_student_ajax(request):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            username = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email')
            password = data.get('password')
            
            # Validate required fields
            if not all([username, first_name, last_name, email, password]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required'
                })
            
            # Check if username exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Username already exists'
                })
            
            # Check if email exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Email already exists'
                })
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Student created successfully',
                'new_student': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'join_date': user.date_joined.strftime("%b %d, %Y")
                },
                'total_students': User.objects.count()
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'accounts/room_list.html', {'rooms': rooms})

def complaint_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Complaint.objects.create(student=request.user, title=title, description=description)
        return redirect('student_complaints')
    return render(request, 'accounts/complaint_create.html')

def fee_payment(request):
    if request.method == 'POST':
        # Add your fee payment logic here
        amount = request.POST.get('amount')
        # Process payment logic
        messages.success(request, 'Fee payment processed successfully')
        return redirect('student_dashboard')
    
    # Get current fee status for the student
    fee_info = Fee.objects.filter(student=request.user).first()
    return render(request, 'accounts/fee_payment.html', {'fee_info': fee_info})

def daily_tasks(request):
    tasks = DailyTask.objects.all()
    return render(request, 'accounts/daily_tasks.html', {'tasks': tasks})

def room_details(request):
    room_allocation = RoomAllocation.objects.filter(student=request.user).first()
    return render(request, 'accounts/room_details.html', {'room_allocation': room_allocation})