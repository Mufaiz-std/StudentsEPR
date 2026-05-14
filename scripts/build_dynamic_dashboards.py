import os
import re

views_code = """
from erp_app.models import StaffAttendance, StaffAttendanceReport

# ===== UPDATE DASHBOARDS WITH DYNAMIC DATA =====
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
def staff_home(request):
    staff = Staff.objects.get(admin=request.user)
    subjects = Subject.objects.filter(staff_id=request.user)
    student_count = Student.objects.filter(course_id__in=[s.course_id for s in subjects]).count()
    subject_count = subjects.count()
    leave_count = LeaveReport.objects.filter(user=request.user).count()
    context = {
        'student_count': student_count,
        'subject_count': subject_count,
        'leave_count': leave_count
    }
    return render(request, 'staff_template/home_content.html', context)

@login_required(login_url='/')
def student_home(request):
    student = Student.objects.get(admin=request.user)
    total_attendance = AttendanceReport.objects.filter(student_id=student).count()
    present_attendance = AttendanceReport.objects.filter(student_id=student, status=True).count()
    attendance_percent = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    subject_count = Subject.objects.filter(course_id=student.course_id).count()
    leave_count = LeaveReport.objects.filter(user=request.user, leave_status=0).count()
    context = {
        'attendance_percent': round(attendance_percent, 2),
        'subject_count': subject_count,
        'leave_count': leave_count
    }
    return render(request, 'student_template/home_content.html', context)

# ===== ADMIN TAKES STAFF ATTENDANCE =====
@login_required(login_url='/')
def admin_staff_attendance(request):
    staffs = Staff.objects.all()
    if request.method == "POST":
        attendance_date = request.POST.get('attendance_date')
        staff_ids = request.POST.getlist('staff_ids')
        
        try:
            attendance = StaffAttendance.objects.create(attendance_date=attendance_date)
            for staff in staffs:
                status = str(staff.id) in staff_ids
                StaffAttendanceReport.objects.create(staff_id=staff, attendance_id=attendance, status=status)
            messages.success(request, 'Staff Attendance Saved Successfully!')
        except Exception as e:
            messages.error(request, f'Error saving attendance: {e}')
        return redirect('admin_staff_attendance')
        
    return render(request, 'admin_template/staff_attendance.html', {'staffs': staffs})

# ===== STAFF VIEWS PERSONAL ATTENDANCE =====
@login_required(login_url='/')
def staff_view_personal_attendance(request):
    staff = Staff.objects.get(admin=request.user)
    reports = StaffAttendanceReport.objects.filter(staff_id=staff).order_by('-attendance_id__attendance_date')
    return render(request, 'staff_template/view_personal_attendance.html', {'reports': reports})

# ===== ADMIN APPROVES/REJECTS STAFF LEAVE =====
@login_required(login_url='/')
def admin_leave_requests(request):
    # Only get leaves for staff (user_type=2)
    staff_users = CustomUser.objects.filter(user_type=2)
    leaves = LeaveReport.objects.filter(user__in=staff_users).order_by('-id')
    return render(request, 'admin_template/leave_requests.html', {'leaves': leaves})

@login_required(login_url='/')
def admin_approve_leave(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    messages.success(request, 'Leave Approved.')
    return redirect('admin_leave_requests')

@login_required(login_url='/')
def admin_reject_leave(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    messages.error(request, 'Leave Rejected.')
    return redirect('admin_leave_requests')

# ===== STAFF APPROVES/REJECTS STUDENT LEAVE =====
@login_required(login_url='/')
def staff_student_leave_requests(request):
    # For simplicity, staff sees all student leaves
    student_users = CustomUser.objects.filter(user_type=3)
    leaves = LeaveReport.objects.filter(user__in=student_users).order_by('-id')
    return render(request, 'staff_template/student_leave_requests.html', {'leaves': leaves})

@login_required(login_url='/')
def staff_approve_leave(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    messages.success(request, 'Student Leave Approved.')
    return redirect('staff_student_leave_requests')

@login_required(login_url='/')
def staff_reject_leave(request, leave_id):
    leave = LeaveReport.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    messages.error(request, 'Student Leave Rejected.')
    return redirect('staff_student_leave_requests')

"""

# Append views
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    content = f.read()

# Replace empty home functions
content = re.sub(r"@login_required\(login_url='/'\)\ndef admin_home\(request\):\n    return render\(request, 'admin_template/home_content\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef staff_home\(request\):\n    return render\(request, 'staff_template/home_content\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef student_home\(request\):\n    return render\(request, 'student_template/home_content\.html'\)", "", content)

with open(views_path, 'w') as f:
    f.write(content + "\n" + views_code)


urls_code = """
    path('admin_staff_attendance/', views.admin_staff_attendance, name="admin_staff_attendance"),
    path('staff_view_personal_attendance/', views.staff_view_personal_attendance, name="staff_view_personal_attendance"),
    
    path('admin_leave_requests/', views.admin_leave_requests, name="admin_leave_requests"),
    path('admin_approve_leave/<int:leave_id>/', views.admin_approve_leave, name="admin_approve_leave"),
    path('admin_reject_leave/<int:leave_id>/', views.admin_reject_leave, name="admin_reject_leave"),
    
    path('staff_student_leave_requests/', views.staff_student_leave_requests, name="staff_student_leave_requests"),
    path('staff_approve_leave/<int:leave_id>/', views.staff_approve_leave, name="staff_approve_leave"),
    path('staff_reject_leave/<int:leave_id>/', views.staff_reject_leave, name="staff_reject_leave"),
"""

urls_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\urls.py"
with open(urls_path, 'r') as f:
    ucontent = f.read()

if "admin_staff_attendance" not in ucontent:
    ucontent = ucontent.replace("]", urls_code + "\n]")
    with open(urls_path, 'w') as f:
        f.write(ucontent)

print("Logic for new features generated.")
