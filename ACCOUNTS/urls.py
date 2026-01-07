from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('login-view/', views.login_view, name='login_view'),

    #student urls
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('student-complaints/', views.student_complaints, name='student_complaints'),
    path('student-fees/', views.student_fees, name='student_fees'),
    path('my-notifications/', views.my_notifications, name='my_notifications'),
    path('trigger-emergency/', views.trigger_emergency, name='trigger_emergency'),
    path('add-student-ajax/', views.add_student_ajax, name='add_student_ajax'),

    #admin/staff urls
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('allocate-room/', views.allocate_room, name='allocate_room'),
    path('fees_dashboard/', views.fees_dashboard, name='fees_dashboard'),
    path('mark-fee-paid/<int:fee_id>/', views.mark_fee_paid, name='mark_fee_paid'),
    path('all-complaints/', views.all_complaints, name='all_complaints'),
    path('resolve-complaint/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('notifications-dashboard/', views.notifications_dashboard, name='notifications_dashboard'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('view-emergencies/', views.view_emergencies, name='view_emergencies'),
    path('resolve-emergency/<int:emergency_id>/', views.resolve_emergency, name='resolve_emergency'),
    path('reports_dashboard/', views.dashboard_reports, name='reports_dashboard'),

    path('login/student/', views.student_login, name='student_login'),
    path('login/staff/', views.staff_login, name='staff_login'),
    path('login/admin/', views.admin_login, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/staff/', views.staff_signup, name='staff_signup'),

   
    path('student_list/', views.student_list, name='student_list'),
    path('room_list/', views.room_list, name='room_list'),
    path('complaint_create/', views.complaint_create, name='complaint_create'),
    path('fee_payment/', views.fee_payment, name='fee_payment'),
    path('daily_tasks/', views.daily_tasks, name='daily_tasks'),
    path('room_details/', views.room_details, name='room_details'),

    # Dashboard URLs - Add these for your HTML files
    path('student-dashboard.html', views.student_dashboard, name='student_dashboard_html'),
    path('staff-dashboard.html', views.staff_dashboard, name='staff_dashboard_html'),
    

]

