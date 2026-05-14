import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser
from management.models import Course, Subject
from staff.models import Staff, StaffAttendance, StaffAttendanceReport
from students.models import Student, Attendance, AttendanceReport, LeaveReport, Feedback


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
        'subject_count': subject_count,
    }
    return render(request, 'management/home_content.html', context)


@login_required(login_url='/')
def add_staff_save(request):
    if request.method != 'POST':
        return redirect('manage_staff')
    try:
        user = CustomUser.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            user_type=2,
        )
        Staff.objects.create(admin=user, address=request.POST.get('address'))
        messages.success(request, 'Staff added successfully!')
    except Exception as e:
        messages.error(request, f'Failed to add staff: {e}')
    return redirect('manage_staff')


@login_required(login_url='/')
def manage_staff(request):
    return render(request, 'management/manage_staff.html', {'staffs': Staff.objects.all()})


@login_required(login_url='/')
def delete_staff(request, staff_id):
    try:
        CustomUser.objects.get(id=staff_id).delete()
        messages.success(request, 'Staff deleted successfully!')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Staff not found.')
    return redirect('manage_staff')


@login_required(login_url='/')
def add_student_save(request):
    if request.method != 'POST':
        return redirect('manage_student')
    try:
        course = Course.objects.get(id=request.POST.get('course_id'))
        user = CustomUser.objects.create_user(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            user_type=3,
        )
        Student.objects.create(
            admin=user,
            address=request.POST.get('address'),
            course_id=course,
        )
        messages.success(request, 'Student added successfully!')
    except Exception as e:
        messages.error(request, f'Failed to add student: {e}')
    return redirect('manage_student')


@login_required(login_url='/')
def manage_student(request):
    return render(request, 'management/manage_student.html', {
        'students': Student.objects.all(),
        'courses': Course.objects.all(),
    })


@login_required(login_url='/')
def delete_student(request, student_id):
    try:
        CustomUser.objects.get(id=student_id).delete()
        messages.success(request, 'Student deleted successfully!')
    except CustomUser.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('manage_student')


@login_required(login_url='/')
def add_course_save(request):
    if request.method == 'POST':
        Course.objects.create(course_name=request.POST.get('course_name'))
        messages.success(request, 'Course added successfully!')
    return redirect('manage_course')


@login_required(login_url='/')
def manage_course(request):
    return render(request, 'management/manage_course.html', {'courses': Course.objects.all()})


@login_required(login_url='/')
def add_subject_save(request):
    if request.method == 'POST':
        Subject.objects.create(
            subject_name=request.POST.get('subject_name'),
            course_id=Course.objects.get(id=request.POST.get('course_id')),
            staff_id=CustomUser.objects.get(id=request.POST.get('staff_id')),
        )
        messages.success(request, 'Subject added successfully!')
    return redirect('manage_subject')


@login_required(login_url='/')
def manage_subject(request):
    return render(request, 'management/manage_subject.html', {
        'subjects': Subject.objects.all(),
        'courses': Course.objects.all(),
        'staffs': CustomUser.objects.filter(user_type=2),
    })


@login_required(login_url='/')
def admin_staff_attendance(request):
    staffs = Staff.objects.all()
    return render(request, 'management/staff_attendance.html', {'staffs': staffs})


@login_required(login_url='/')
def admin_save_staff_attendance_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        attendance_date = data.get('attendance_date')
        staff_ids = data.get('staff_ids', [])

        attendance = StaffAttendance.objects.create(attendance_date=attendance_date)
        for staff in Staff.objects.all():
            StaffAttendanceReport.objects.create(
                staff_id=staff,
                attendance_id=attendance,
                status=str(staff.id) in staff_ids,
            )

        return JsonResponse({'message': 'Staff attendance saved successfully!'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='/')
def admin_leave_requests(request):
    return render(request, 'management/leave_requests.html', {
        'leaves': LeaveReport.objects.filter(user__user_type=2).order_by('-id'),
    })


@login_required(login_url='/')
def admin_approve_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=1)
    messages.success(request, 'Leave approved.')
    return redirect('admin_leave_requests')


@login_required(login_url='/')
def admin_reject_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=2)
    messages.error(request, 'Leave rejected.')
    return redirect('admin_leave_requests')


@login_required(login_url='/')
def admin_feedback_message(request):
    return render(request, 'management/feedback_message.html', {
        'feedbacks': Feedback.objects.all(),
    })
