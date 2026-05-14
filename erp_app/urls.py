from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name="login_page"),
    path('doLogin/', views.do_login, name="do_login"),
    path('logout_user/', views.logout_user, name="logout_user"),
    
    # Admin
    path('admin_home/', views.admin_home, name="admin_home"),
    path('manage_staff/', views.manage_staff, name="manage_staff"),
    path('manage_student/', views.manage_student, name="manage_student"),
    path('manage_course/', views.manage_course, name="manage_course"),
    path('manage_subject/', views.manage_subject, name="manage_subject"),
    
    # Staff
    path('staff_home/', views.staff_home, name="staff_home"),
    path('staff_take_attendance/', views.staff_take_attendance, name="staff_take_attendance"),
    path('staff_apply_leave/', views.staff_apply_leave, name="staff_apply_leave"),
    path('staff_feedback/', views.staff_feedback, name="staff_feedback"),
    
    # Student
    path('student_home/', views.student_home, name="student_home"),
    path('student_view_attendance/', views.student_view_attendance, name="student_view_attendance"),
    path('student_apply_leave/', views.student_apply_leave, name="student_apply_leave"),
    path('student_feedback/', views.student_feedback, name="student_feedback"),

    path('add_staff_save/', views.add_staff_save, name="add_staff_save"),
    path('add_student_save/', views.add_student_save, name="add_student_save"),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name="delete_staff"),
    path('delete_student/<int:student_id>/', views.delete_student, name="delete_student"),
    path('admin_feedback_message/', views.admin_feedback_message, name="admin_feedback_message"),


    path('staff_feedback_save/', views.staff_feedback_save, name="staff_feedback_save"),
    path('student_feedback_save/', views.student_feedback_save, name="student_feedback_save"),
    path('staff_leave_save/', views.staff_leave_save, name="staff_leave_save"),
    path('student_leave_save/', views.student_leave_save, name="student_leave_save"),


    path('add_course_save/', views.add_course_save, name="add_course_save"),
    path('add_subject_save/', views.add_subject_save, name="add_subject_save"),


    path('profile/', views.profile_view, name="profile_view"),
    path('staff_view_attendance/', views.staff_view_attendance, name="staff_view_attendance"),


    path('admin_staff_attendance/', views.admin_staff_attendance, name="admin_staff_attendance"),
    path('staff_view_personal_attendance/', views.staff_view_personal_attendance, name="staff_view_personal_attendance"),
    
    path('admin_leave_requests/', views.admin_leave_requests, name="admin_leave_requests"),
    path('admin_approve_leave/<int:leave_id>/', views.admin_approve_leave, name="admin_approve_leave"),
    path('admin_reject_leave/<int:leave_id>/', views.admin_reject_leave, name="admin_reject_leave"),
    
    path('staff_student_leave_requests/', views.staff_student_leave_requests, name="staff_student_leave_requests"),
    path('staff_approve_leave/<int:leave_id>/', views.staff_approve_leave, name="staff_approve_leave"),
    path('staff_reject_leave/<int:leave_id>/', views.staff_reject_leave, name="staff_reject_leave"),

]
