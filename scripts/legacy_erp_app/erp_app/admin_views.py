from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from management.models import Course, Subject
from staff.models import Staff, StaffAttendance, StaffAttendanceReport
from students.models import Student, Attendance, AttendanceReport, LeaveReport, Feedback, Notification


@login_required(login_url='/')
def admin_home(request):
    staff_count = Staff.objects.all().count()
    student_count = Student.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    context = {
        'staff_count': staff_count,
        'student_count': student_count,
        'course_count': course_count,
        'subject_count': subject_count
    }
    return render(request, 'admin_template/home_content.html', context)

@login_required(login_url='/')
def add_staff_save(request):
    if request.method != "POST": return redirect('manage_staff')
    try:
        user = CustomUser.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'), email=request.POST.get('email'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'), user_type=2)
        Staff.objects.create(admin=user, address=request.POST.get('address'))
        messages.success(request, 'Staff Added Successfully!')
    except Exception as e:
        messages.error(request, f'Failed to Add Staff: {e}')
    return redirect('manage_staff')

@login_required(login_url='/')
def manage_staff(request):
    return render(request, 'admin_template/manage_staff.html', {'staffs': Staff.objects.all()})

@login_required(login_url='/')
def delete_staff(request, staff_id):
    try: CustomUser.objects.get(id=staff_id).delete(); messages.success(request, 'Staff Deleted Successfully!')
    except: messages.error(request, 'Failed to Delete Staff.')
    return redirect('manage_staff')

@login_required(login_url='/')
def add_student_save(request):
    if request.method != "POST": return redirect('manage_student')
    try:
        course = Course.objects.get(id=request.POST.get('course_id'))
        user = CustomUser.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'), email=request.POST.get('email'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'), user_type=3)
        Student.objects.create(admin=user, address=request.POST.get('address'), course_id=course)
        messages.success(request, 'Student Added Successfully!')
    except Exception as e:
        messages.error(request, f'Failed to Add Student: {e}')
    return redirect('manage_student')

@login_required(login_url='/')
def manage_student(request):
    return render(request, 'admin_template/manage_student.html', {'students': Student.objects.all(), 'courses': Course.objects.all()})

@login_required(login_url='/')
def delete_student(request, student_id):
    try: CustomUser.objects.get(id=student_id).delete(); messages.success(request, 'Student Deleted Successfully!')
    except: messages.error(request, 'Failed to Delete Student.')
    return redirect('manage_student')

@login_required(login_url='/')
def add_course_save(request):
    if request.method == "POST":
        Course.objects.create(course_name=request.POST.get('course_name'))
        messages.success(request, 'Course Added Successfully!')
    return redirect('manage_course')

@login_required(login_url='/')
def manage_course(request):
    return render(request, 'admin_template/manage_course.html', {'courses': Course.objects.all()})

@login_required(login_url='/')
def add_subject_save(request):
    if request.method == "POST":
        Subject.objects.create(subject_name=request.POST.get('subject_name'), course_id=Course.objects.get(id=request.POST.get('course_id')), staff_id=CustomUser.objects.get(id=request.POST.get('staff_id')))
        messages.success(request, 'Subject Added Successfully!')
    return redirect('manage_subject')

@login_required(login_url='/')
def manage_subject(request):
    return render(request, 'admin_template/manage_subject.html', {'subjects': Subject.objects.all(), 'courses': Course.objects.all(), 'staffs': CustomUser.objects.filter(user_type=2)})

@login_required(login_url='/')
def admin_staff_attendance(request):
    staffs = Staff.objects.all()
    if request.method == "POST":
        attendance = StaffAttendance.objects.create(attendance_date=request.POST.get('attendance_date'))
        for staff in staffs:
            StaffAttendanceReport.objects.create(staff_id=staff, attendance_id=attendance, status=str(staff.id) in request.POST.getlist('staff_ids'))
        messages.success(request, 'Staff Attendance Saved Successfully!')
        return redirect('admin_staff_attendance')
    return render(request, 'admin_template/staff_attendance.html', {'staffs': staffs})

@login_required(login_url='/')
def admin_leave_requests(request):
    return render(request, 'admin_template/leave_requests.html', {'leaves': LeaveReport.objects.filter(user__user_type=2).order_by('-id')})

@login_required(login_url='/')
def admin_approve_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=1)
    messages.success(request, 'Leave Approved.')
    return redirect('admin_leave_requests')

@login_required(login_url='/')
def admin_reject_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=2)
    messages.error(request, 'Leave Rejected.')
    return redirect('admin_leave_requests')

@login_required(login_url='/')
def admin_feedback_message(request):
    return render(request, 'admin_template/feedback_message.html', {'feedbacks': Feedback.objects.all()})
