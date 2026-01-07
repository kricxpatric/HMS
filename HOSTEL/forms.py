# hostel/forms.py
from django import forms
from ACCOUNTS.models import User
from .models import Student, Room

class StudentForm(forms.ModelForm):
    # User account fields
    username = forms.CharField(
        max_length=150, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter password'
        }),
        required=True
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'Enter last name'
        })
    )
    
    class Meta:
        model = Student
        fields = ['roll_no', 'phone']
        widgets = {
            'roll_no': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Enter roll number'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Enter phone number'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists!")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!")
        return email
    
    def clean_roll_no(self):
        roll_no = self.cleaned_data['roll_no']
        if Student.objects.filter(roll_no=roll_no).exists():
            raise forms.ValidationError("Roll number already exists!")
        return roll_no
    
    def save(self, commit=True):
        # Create User account first
        user_data = {
            'username': self.cleaned_data['username'],
            'email': self.cleaned_data['email'],
            'first_name': self.cleaned_data['first_name'],
            'last_name': self.cleaned_data['last_name'],
            'role': 'student'
        }
        
        user = User.objects.create_user(**user_data)
        user.set_password(self.cleaned_data['password'])
        user.save()
        
        # Create Student profile
        student = super().save(commit=False)
        student.name = f"{user.first_name} {user.last_name}"
        student.email = user.email
        
        if commit:
            student.save()
        
        return student

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        widgets = {
            'room_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Enter room number'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Enter room capacity'
            }),
        }
