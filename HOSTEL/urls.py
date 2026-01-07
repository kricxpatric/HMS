from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/edit/<int:id>/', views.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('students/allocate_room/', views.allocate_room, name='allocate_room'),
    
    # Room URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:id>/', views.edit_room, name='edit_room'),
    path('rooms/delete/<int:id>/', views.delete_room, name='delete_room'),
]
