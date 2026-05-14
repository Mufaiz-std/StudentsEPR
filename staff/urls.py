from django.urls import path
from . import views

urlpatterns = [
    path('', views.staff_home, name='staff_home'),
    path('take_attendance/', views.staff_take_attendance, name='staff_take_attendance'),
    path('save_attendance/', views.staff_save_attendance_api, name='staff_save_attendance_api'),
    path('view_attendance/', views.staff_view_attendance, name='staff_view_attendance'),
    path('view_personal_attendance/', views.staff_view_personal_attendance, name='staff_view_personal_attendance'),
    path('student_leave_requests/', views.staff_student_leave_requests, name='staff_student_leave_requests'),
    path('approve_leave/<int:leave_id>/', views.staff_approve_leave, name='staff_approve_leave'),
    path('reject_leave/<int:leave_id>/', views.staff_reject_leave, name='staff_reject_leave'),
    path('apply_leave/', views.staff_apply_leave, name='staff_apply_leave'),
    path('leave_save/', views.staff_leave_save, name='staff_leave_save'),
    path('feedback/', views.staff_feedback, name='staff_feedback'),
    path('feedback_save/', views.staff_feedback_save, name='staff_feedback_save'),
]
