"""
URL configuration for HMS_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from ACCOUNTS import views as accounts_views
from HOSTEL import views as hostel_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accounts_views.home, name='home'),  # Make login page root
    path('', include('ACCOUNTS.urls')),       # include other account URLs
    path('hostel/', include('HOSTEL.urls')),

    path('students/', hostel_views.student_list, name='student_list'),
    path('students/add/', hostel_views.add_student, name='add_student'),
    path('students/edit/<int:id>/', hostel_views.edit_student, name='edit_student'),
    path('students/delete/<int:id>/', hostel_views.delete_student, name='delete_student'),
]
