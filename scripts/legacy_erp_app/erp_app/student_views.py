from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from management.models import Course, Subject
from staff.models import Staff, StaffAttendance, StaffAttendanceReport
from students.models import Student, Attendance, AttendanceReport, LeaveReport, Feedback, Notification


@login_required(login_url='/')
def student_home(request):
    student = Student.objects.get(admin=request.user)
    total_attendance = AttendanceReport.objects.filter(student_id=student).count()
    present_attendance = AttendanceReport.objects.filter(student_id=student, status=True).count()
    attendance_percent = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    context = {
        'attendance_percent': round(attendance_percent, 2),
        'subject_count': Subject.objects.filter(course_id=student.course_id).count(),
        'leave_count': LeaveReport.objects.filter(user=request.user, leave_status=0).count()
    }
    return render(request, 'student_template/home_content.html', context)

@login_required(login_url='/')
def student_view_attendance(request):
    return render(request, 'student_template/view_attendance.html', {'reports': AttendanceReport.objects.filter(student_id__admin=request.user).order_by('-attendance_id__attendance_date')})

@login_required(login_url='/')
def student_apply_leave(request):
    return render(request, 'student_template/apply_leave.html', {'leaves': LeaveReport.objects.filter(user=request.user)})

@login_required(login_url='/')
def student_leave_save(request):
    if request.method == "POST":
        LeaveReport.objects.create(user=request.user, leave_date=request.POST.get('leave_date'), leave_message=request.POST.get('leave_msg'))
        messages.success(request, 'Leave Application Submitted!')
    return redirect('student_apply_leave')

@login_required(login_url='/')
def student_feedback(request):
    return render(request, 'student_template/feedback.html', {'feedbacks': Feedback.objects.filter(user=request.user)})

@login_required(login_url='/')
def student_feedback_save(request):
    if request.method == "POST":
        Feedback.objects.create(user=request.user, feedback=request.POST.get('feedback_msg'))
        messages.success(request, 'Feedback Sent Successfully!')
    return redirect('student_feedback')
