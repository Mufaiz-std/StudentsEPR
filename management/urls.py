from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),
    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('add_staff_save/', views.add_staff_save, name='add_staff_save'),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('manage_student/', views.manage_student, name='manage_student'),
    path('add_student_save/', views.add_student_save, name='add_student_save'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('manage_course/', views.manage_course, name='manage_course'),
    path('add_course_save/', views.add_course_save, name='add_course_save'),
    path('manage_subject/', views.manage_subject, name='manage_subject'),
    path('add_subject_save/', views.add_subject_save, name='add_subject_save'),
    path('admin_staff_attendance/', views.admin_staff_attendance, name='admin_staff_attendance'),
    path('save_staff_attendance/', views.admin_save_staff_attendance_api, name='admin_save_staff_attendance_api'),
    path('admin_leave_requests/', views.admin_leave_requests, name='admin_leave_requests'),
    path('admin_approve_leave/<int:leave_id>/', views.admin_approve_leave, name='admin_approve_leave'),
    path('admin_reject_leave/<int:leave_id>/', views.admin_reject_leave, name='admin_reject_leave'),
    path('admin_feedback_message/', views.admin_feedback_message, name='admin_feedback_message'),
]
