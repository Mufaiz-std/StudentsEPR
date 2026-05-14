import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from management.models import Subject
from staff.models import Staff, StaffAttendance, StaffAttendanceReport
from students.models import Student, Attendance, AttendanceReport, LeaveReport, Feedback


@login_required(login_url='/')
def staff_home(request):
    staff = Staff.objects.get(admin=request.user)
    subjects = Subject.objects.filter(staff_id=request.user)
    context = {
        'student_count': Student.objects.filter(course_id__in=[s.course_id for s in subjects]).count(),
        'subject_count': subjects.count(),
        'leave_count': LeaveReport.objects.filter(user=request.user).count(),
    }
    return render(request, 'staff/home_content.html', context)


@login_required(login_url='/')
def staff_take_attendance(request):
    subjects = Subject.objects.filter(staff_id=request.user)
    return render(request, 'staff/take_attendance.html', {
        'subjects': subjects,
        'students': Student.objects.all(),
    })


@login_required(login_url='/')
def staff_save_attendance_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        subject_id = data.get('subject_id')
        attendance_date = data.get('attendance_date')
        student_ids = data.get('student_ids', [])

        subject = Subject.objects.get(id=subject_id)
        attendance = Attendance.objects.create(subject_id=subject, attendance_date=attendance_date)

        for student in Student.objects.filter(course_id=subject.course_id):
            status = str(student.id) in student_ids
            AttendanceReport.objects.create(
                student_id=student,
                attendance_id=attendance,
                status=status,
            )

        return JsonResponse({'message': 'Attendance saved successfully!'}, status=200)
    except Subject.DoesNotExist:
        return JsonResponse({'error': 'Selected subject does not exist.'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required(login_url='/')
def staff_view_attendance(request):
    return render(request, 'staff/view_attendance.html', {
        'attendances': Attendance.objects.filter(subject_id__staff_id=request.user).order_by('-attendance_date'),
    })


@login_required(login_url='/')
def staff_view_personal_attendance(request):
    return render(request, 'staff/view_personal_attendance.html', {
        'reports': StaffAttendanceReport.objects.filter(staff_id__admin=request.user).order_by('-attendance_id__attendance_date'),
    })


@login_required(login_url='/')
def staff_student_leave_requests(request):
    return render(request, 'staff/student_leave_requests.html', {
        'leaves': LeaveReport.objects.filter(user__user_type=3).order_by('-id'),
    })


@login_required(login_url='/')
def staff_approve_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=1)
    messages.success(request, 'Student leave approved.')
    return redirect('staff_student_leave_requests')


@login_required(login_url='/')
def staff_reject_leave(request, leave_id):
    LeaveReport.objects.filter(id=leave_id).update(leave_status=2)
    messages.error(request, 'Student leave rejected.')
    return redirect('staff_student_leave_requests')


@login_required(login_url='/')
def staff_apply_leave(request):
    return render(request, 'staff/apply_leave.html', {
        'leaves': LeaveReport.objects.filter(user=request.user),
    })


@login_required(login_url='/')
def staff_leave_save(request):
    if request.method == 'POST':
        LeaveReport.objects.create(
            user=request.user,
            leave_date=request.POST.get('leave_date'),
            leave_message=request.POST.get('leave_msg'),
        )
        messages.success(request, 'Leave application submitted!')
    return redirect('staff_apply_leave')


@login_required(login_url='/')
def staff_feedback(request):
    return render(request, 'staff/feedback.html', {
        'feedbacks': Feedback.objects.filter(user=request.user),
    })


@login_required(login_url='/')
def staff_feedback_save(request):
    if request.method == 'POST':
        Feedback.objects.create(user=request.user, feedback=request.POST.get('feedback_msg'))
        messages.success(request, 'Feedback sent successfully!')
    return redirect('staff_feedback')
