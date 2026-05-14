from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from management.models import Course, Subject
from staff.models import Staff, StaffAttendance, StaffAttendanceReport
from students.models import Student, Attendance, AttendanceReport, LeaveReport, Feedback, Notification


@login_required(login_url='/')
def staff_home(request):
    staff = Staff.objects.get(admin=request.user)
    subjects = Subject.objects.filter(staff_id=request.user)
    context = {
        'student_count': Student.objects.filter(course_id__in=[s.course_id for s in subjects]).count(),
        'subject_count': subjects.count(),
        'leave_count': LeaveReport.objects.filter(user=request.user).count()
    }
    return render(request, 'staff_template/home_content.html', context)

@login_required(login_url='/')
def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user)
    if request.method == "POST":
        subject = Subject.objects.get(id=request.POST.get('subject_id'))
        attendance = Attendance.objects.create(subject_id=subject, attendance_date=request.POST.get('attendance_date'))
        student_ids = request.POST.getlist('student_ids')
        for student in Student.objects.filter(course_id=subject.course_id):
            AttendanceReport.objects.create(student_id=student, attendance_id=attendance, status=str(student.id) in student_ids)
        messages.success(request, 'Attendance Saved Successfully!')
        return redirect('staff_take_attendance')
    return render(request, 'staff_template/take_attendance.html', {'subjects': subjects, 'students': Student.objects.all()})

@login_required(login_url='/')
def staff_view_attendance(request):
    return render(request, 'staff_template/view_attendance.html', {'attendances': Attendance.objects.filter(subject_id__staff_id=request.user).order_by('-attendance_date')})

@login_required(login_url='/')
def staff_view_personal_attendance(request):
    return render(request, 'staff_template/view_personal_attendance.html', {'reports': StaffAttendanceReport.objects.filter(staff_id__admin=request.user).order_by('-attendance_id__attendance_date')})

@login_required(login_url='/')
def staff_student_leave_requests(request):
    return render(request, 'staff_template/student_leave_requests.html', {'leaves': LeaveReport.objects.filter(user__user_type=3).order_by('-id')})

@login_required(login_url='/')
def staff_approve_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=1)
    messages.success(request, 'Student Leave Approved.')
    return redirect('staff_student_leave_requests')

@login_required(login_url='/')
def staff_reject_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=2)
    messages.error(request, 'Student Leave Rejected.')
    return redirect('staff_student_leave_requests')

@login_required(login_url='/')
def staff_apply_leave(request):
    return render(request, 'staff_template/apply_leave.html', {'leaves': LeaveReport.objects.filter(user=request.user)})

@login_required(login_url='/')
def staff_leave_save(request):
    if request.method == "POST":
        LeaveReport.objects.create(user=request.user, leave_date=request.POST.get('leave_date'), leave_message=request.POST.get('leave_msg'))
        messages.success(request, 'Leave Application Submitted!')
    return redirect('staff_apply_leave')

@login_required(login_url='/')
def staff_feedback(request):
    return render(request, 'staff_template/feedback.html', {'feedbacks': Feedback.objects.filter(user=request.user)})

@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == "POST":
        Feedback.objects.create(user=request.user, feedback=request.POST.get('feedback_msg'))
        messages.success(request, 'Feedback Sent Successfully!')
    return redirect('staff_feedback')
