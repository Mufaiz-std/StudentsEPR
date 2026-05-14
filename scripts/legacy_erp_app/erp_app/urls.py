
from django.urls import path
from . import views, admin_views, staff_views, student_views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('doLogin/', views.do_login, name="do_login"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('profile/', views.profile_view, name="profile_view"),
    
    # Admin
    path('admin_home/', admin_views.admin_home, name="admin_home"),
    path('manage_staff/', admin_views.manage_staff, name="manage_staff"),
    path('add_staff_save/', admin_views.add_staff_save, name="add_staff_save"),
    path('delete_staff/<int:staff_id>/', admin_views.delete_staff, name="delete_staff"),
    
    path('manage_student/', admin_views.manage_student, name="manage_student"),
    path('add_student_save/', admin_views.add_student_save, name="add_student_save"),
    path('delete_student/<int:student_id>/', admin_views.delete_student, name="delete_student"),
    
    path('manage_course/', admin_views.manage_course, name="manage_course"),
    path('add_course_save/', admin_views.add_course_save, name="add_course_save"),
    
    path('manage_subject/', admin_views.manage_subject, name="manage_subject"),
    path('add_subject_save/', admin_views.add_subject_save, name="add_subject_save"),
    
    path('admin_staff_attendance/', admin_views.admin_staff_attendance, name="admin_staff_attendance"),
    
    path('admin_leave_requests/', admin_views.admin_leave_requests, name="admin_leave_requests"),
    path('admin_approve_leave/<int:leave_id>/', admin_views.admin_approve_leave, name="admin_approve_leave"),
    path('admin_reject_leave/<int:leave_id>/', admin_views.admin_reject_leave, name="admin_reject_leave"),
    
    path('admin_feedback_message/', admin_views.admin_feedback_message, name="admin_feedback_message"),

    # Staff
    path('staff_home/', staff_views.staff_home, name="staff_home"),
    path('staff_take_attendance/', staff_views.staff_take_attendance, name="staff_take_attendance"),
    path('staff_view_attendance/', staff_views.staff_view_attendance, name="staff_view_attendance"),
    path('staff_view_personal_attendance/', staff_views.staff_view_personal_attendance, name="staff_view_personal_attendance"),
    
    path('staff_student_leave_requests/', staff_views.staff_student_leave_requests, name="staff_student_leave_requests"),
    path('staff_approve_leave/<int:leave_id>/', staff_views.staff_approve_leave, name="staff_approve_leave"),
    path('staff_reject_leave/<int:leave_id>/', staff_views.staff_reject_leave, name="staff_reject_leave"),
    
    path('staff_apply_leave/', staff_views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_leave_save/', staff_views.staff_leave_save, name="staff_leave_save"),
    path('staff_feedback/', staff_views.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', staff_views.staff_feedback_save, name="staff_feedback_save"),

    # Student
    path('student_home/', student_views.student_home, name="student_home"),
    path('student_view_attendance/', student_views.student_view_attendance, name="student_view_attendance"),
    path('student_apply_leave/', student_views.student_apply_leave, name="student_apply_leave"),
    path('student_leave_save/', student_views.student_leave_save, name="student_leave_save"),
    path('student_feedback/', student_views.student_feedback, name="student_feedback"),
    path('student_feedback_save/', student_views.student_feedback_save, name="student_feedback_save"),
]
