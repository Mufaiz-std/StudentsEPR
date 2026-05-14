from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_home, name='student_home'),
    path('view_attendance/', views.student_view_attendance, name='student_view_attendance'),
    path('apply_leave/', views.student_apply_leave, name='student_apply_leave'),
    path('leave_save/', views.student_leave_save, name='student_leave_save'),
    path('feedback/', views.student_feedback, name='student_feedback'),
    path('feedback_save/', views.student_feedback_save, name='student_feedback_save'),
]
