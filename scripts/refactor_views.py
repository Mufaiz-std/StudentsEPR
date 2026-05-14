import os
import re

# 1. Read the entire views.py
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    views_content = f.read()

# 2. Extract imports
imports = """from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Staff, Student, Course, Subject, LeaveReport, Feedback, Notification, Attendance, AttendanceReport, StaffAttendance, StaffAttendanceReport
"""

# 3. We'll leave login/logout in views.py, and profile.
core_views = """
def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect('admin_home')
        elif request.user.user_type == 2:
            return redirect('staff_home')
        elif request.user.user_type == 3:
            return redirect('student_home')
    return render(request, 'login.html')

def do_login(request):
    if request.method != "POST":
        return redirect('login_page')
    else:
        user_name = request.POST.get('username')
        user_pass = request.POST.get('password')
        user = authenticate(request, username=user_name, password=user_pass)
        if user is not None:
            login(request, user)
            if user.user_type == 1:
                return redirect('admin_home')
            elif user.user_type == 2:
                return redirect('staff_home')
            elif user.user_type == 3:
                return redirect('student_home')
            else:
                return redirect('login_page')
        else:
            messages.error(request, 'Invalid Login Details')
            return redirect('login_page')

def logout_user(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='/')
def profile_view(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        
        user.first_name = first_name
        user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Updated Successfully!')
        return redirect('profile_view')
        
    return render(request, 'profile.html', {'user': user})
"""

# We'll extract admin logic
admin_code = """
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
"""

staff_code = """
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
"""

student_code = """
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
"""

app_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app"

with open(os.path.join(app_path, "views.py"), "w") as f:
    f.write(imports + core_views)

with open(os.path.join(app_path, "admin_views.py"), "w") as f:
    f.write(imports + admin_code)

with open(os.path.join(app_path, "staff_views.py"), "w") as f:
    f.write(imports + staff_code)

with open(os.path.join(app_path, "student_views.py"), "w") as f:
    f.write(imports + student_code)


urls_code = """
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
"""
with open(os.path.join(app_path, "urls.py"), "w") as f:
    f.write(urls_code)

print("Refactored into admin_views.py, staff_views.py, student_views.py successfully.")
