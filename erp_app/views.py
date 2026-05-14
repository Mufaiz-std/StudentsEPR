from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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







# Admin Views








# Staff Views






# Student Views








from .models import CustomUser, Staff, Student, Course, Subject, LeaveReport, Feedback, Notification

# ===== ADMIN CRUD =====
@login_required(login_url='/')
def add_staff_save(request):
    if request.method != "POST":
        return redirect('manage_staff')
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
        Staff.objects.create(admin=user, address=address)
        messages.success(request, 'Staff Added Successfully!')
    except Exception as e:
        messages.error(request, f'Failed to Add Staff: {e}')
    return redirect('manage_staff')

@login_required(login_url='/')
def add_student_save(request):
    if request.method != "POST":
        return redirect('manage_student')
    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        course_id = request.POST.get('course_id')
        
        course = Course.objects.get(id=course_id)
        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
        Student.objects.create(admin=user, address=address, course_id=course)
        messages.success(request, 'Student Added Successfully!')
    except Exception as e:
        messages.error(request, f'Failed to Add Student: {e}')
    return redirect('manage_student')

@login_required(login_url='/')
def delete_staff(request, staff_id):
    try:
        staff = CustomUser.objects.get(id=staff_id)
        staff.delete()
        messages.success(request, 'Staff Deleted Successfully!')
    except:
        messages.error(request, 'Failed to Delete Staff.')
    return redirect('manage_staff')

@login_required(login_url='/')
def delete_student(request, student_id):
    try:
        student = CustomUser.objects.get(id=student_id)
        student.delete()
        messages.success(request, 'Student Deleted Successfully!')
    except:
        messages.error(request, 'Failed to Delete Student.')
    return redirect('manage_student')

# Ensure manage_staff and manage_student actually pass data
@login_required(login_url='/')
def manage_staff(request):
    staffs = Staff.objects.all()
    return render(request, 'admin_template/manage_staff.html', {'staffs': staffs})

@login_required(login_url='/')
def manage_student(request):
    students = Student.objects.all()
    courses = Course.objects.all()
    return render(request, 'admin_template/manage_student.html', {'students': students, 'courses': courses})

# Provide notifications and feedback view for Admin
@login_required(login_url='/')
def admin_feedback_message(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'admin_template/feedback_message.html', {'feedbacks': feedbacks})


# ===== STAFF & STUDENT FEEDBACK/LEAVE =====
@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == "POST":
        feedback_msg = request.POST.get('feedback_msg')
        Feedback.objects.create(user=request.user, feedback=feedback_msg)
        messages.success(request, 'Feedback Sent Successfully!')
    return redirect('staff_feedback')

@login_required(login_url='/')
def student_feedback_save(request):
    if request.method == "POST":
        feedback_msg = request.POST.get('feedback_msg')
        Feedback.objects.create(user=request.user, feedback=feedback_msg)
        messages.success(request, 'Feedback Sent Successfully!')
    return redirect('student_feedback')

@login_required(login_url='/')
def staff_leave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_msg = request.POST.get('leave_msg')
        LeaveReport.objects.create(user=request.user, leave_date=leave_date, leave_message=leave_msg)
        messages.success(request, 'Leave Application Submitted!')
    return redirect('staff_apply_leave')

@login_required(login_url='/')
def student_leave_save(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_msg = request.POST.get('leave_msg')
        LeaveReport.objects.create(user=request.user, leave_date=leave_date, leave_message=leave_msg)
        messages.success(request, 'Leave Application Submitted!')
    return redirect('student_apply_leave')

# Redefine the templates mapping to show past feedback
@login_required(login_url='/')
def staff_feedback(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'staff_template/feedback.html', {'feedbacks': feedbacks})

@login_required(login_url='/')
def student_feedback(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    return render(request, 'student_template/feedback.html', {'feedbacks': feedbacks})

@login_required(login_url='/')
def staff_apply_leave(request):
    leaves = LeaveReport.objects.filter(user=request.user)
    return render(request, 'staff_template/apply_leave.html', {'leaves': leaves})

@login_required(login_url='/')
def student_apply_leave(request):
    leaves = LeaveReport.objects.filter(user=request.user)
    return render(request, 'student_template/apply_leave.html', {'leaves': leaves})



# ===== COURSE & SUBJECT CRUD =====
@login_required(login_url='/')
def add_course_save(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')
        Course.objects.create(course_name=course_name)
        messages.success(request, 'Course Added Successfully!')
    return redirect('manage_course')

@login_required(login_url='/')
def add_subject_save(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        
        course = Course.objects.get(id=course_id)
        staff = CustomUser.objects.get(id=staff_id)
        Subject.objects.create(subject_name=subject_name, course_id=course, staff_id=staff)
        messages.success(request, 'Subject Added Successfully!')
    return redirect('manage_subject')

@login_required(login_url='/')
def manage_course(request):
    courses = Course.objects.all()
    return render(request, 'admin_template/manage_course.html', {'courses': courses})

@login_required(login_url='/')
def manage_subject(request):
    subjects = Subject.objects.all()
    courses = Course.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'admin_template/manage_subject.html', {'subjects': subjects, 'courses': courses, 'staffs': staffs})



from erp_app.models import Attendance, AttendanceReport

# ===== PROFILE VIEWS =====
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

# ===== ATTENDANCE VIEWS =====
@login_required(login_url='/')
def staff_take_attendance(request):
    staff = Staff.objects.get(admin=request.user)
    subjects = Subject.objects.filter(staff_id=request.user)
    
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        attendance_date = request.POST.get('attendance_date')
        student_ids = request.POST.getlist('student_ids') # list of student ids marked present
        
        try:
            subject = Subject.objects.get(id=subject_id)
            # Create Attendance
            attendance = Attendance.objects.create(subject_id=subject, attendance_date=attendance_date)
            
            # Create Attendance Report for all students in the course
            all_students = Student.objects.filter(course_id=subject.course_id)
            for student in all_students:
                status = str(student.id) in student_ids
                AttendanceReport.objects.create(student_id=student, attendance_id=attendance, status=status)
            messages.success(request, 'Attendance Saved Successfully!')
        except Exception as e:
            messages.error(request, f'Error saving attendance: {e}')
        return redirect('staff_take_attendance')

    # Quick helper: just pass all students so they can be rendered. 
    # In a real AJAX app, students load dynamically based on subject.
    # Here we'll just group them by course in the template for simplicity.
    students = Student.objects.all()
    return render(request, 'staff_template/take_attendance.html', {'subjects': subjects, 'students': students})

@login_required(login_url='/')
def staff_view_attendance(request):
    staff_subjects = Subject.objects.filter(staff_id=request.user)
    attendances = Attendance.objects.filter(subject_id__in=staff_subjects).order_by('-attendance_date')
    return render(request, 'staff_template/view_attendance.html', {'attendances': attendances})

@login_required(login_url='/')
def student_view_attendance(request):
    student = Student.objects.get(admin=request.user)
    reports = AttendanceReport.objects.filter(student_id=student).order_by('-attendance_id__attendance_date')
    return render(request, 'student_template/view_attendance.html', {'reports': reports})


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

