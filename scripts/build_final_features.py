import os
import re

views_code = """
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
"""

# Append views
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    content = f.read()

# Replace empty functions to avoid duplicates
content = re.sub(r"@login_required\(login_url='/'\)\ndef staff_take_attendance\(request\):\n    return render\(request, 'staff_template/take_attendance\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef student_view_attendance\(request\):\n    return render\(request, 'student_template/view_attendance\.html'\)", "", content)

with open(views_path, 'w') as f:
    f.write(content + "\n" + views_code)


urls_code = """
    path('profile/', views.profile_view, name="profile_view"),
    path('staff_view_attendance/', views.staff_view_attendance, name="staff_view_attendance"),
"""

urls_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\urls.py"
with open(urls_path, 'r') as f:
    ucontent = f.read()

if "profile_view" not in ucontent:
    ucontent = ucontent.replace("]", urls_code + "\n]")
    with open(urls_path, 'w') as f:
        f.write(ucontent)

# Templates
profile_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; max-width: 600px; margin: auto;">
    <h2>My Profile</h2>
    <form action="{% url 'profile_view' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <label>Username</label>
        <input type="text" value="{{ user.username }}" disabled class="form-input" style="background: #f3f4f6; margin-bottom: 15px;">
        
        <label>Email</label>
        <input type="email" value="{{ user.email }}" disabled class="form-input" style="background: #f3f4f6; margin-bottom: 15px;">

        <label>First Name</label>
        <input type="text" name="first_name" value="{{ user.first_name }}" class="form-input" style="margin-bottom: 15px;">

        <label>Last Name</label>
        <input type="text" name="last_name" value="{{ user.last_name }}" class="form-input" style="margin-bottom: 15px;">

        <label>Change Password (Leave blank to keep current)</label>
        <input type="password" name="password" placeholder="New Password" class="form-input" style="margin-bottom: 15px;">

        <button type="submit" class="btn-primary" style="margin-top: 15px;">Update Profile</button>
    </form>
</div>
{% endblock %}
"""

take_attendance_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Take Attendance</h2>
    <form action="{% url 'staff_take_attendance' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <label>Select Subject</label>
        <select name="subject_id" required class="form-input" style="margin-bottom: 15px;">
            {% for subject in subjects %}<option value="{{ subject.id }}">{{ subject.subject_name }} ({{ subject.course_id.course_name }})</option>{% endfor %}
        </select>
        
        <label>Attendance Date</label>
        <input type="date" name="attendance_date" required class="form-input" style="margin-bottom: 15px;">
        
        <h3>Select Students (Check if Present)</h3>
        <div style="margin-top: 15px; max-height: 300px; overflow-y: auto; border: 1px solid var(--border-color); padding: 10px; border-radius: 6px;">
            {% for student in students %}
            <div style="margin-bottom: 10px;">
                <label>
                    <input type="checkbox" name="student_ids" value="{{ student.id }}" style="margin-right: 10px;">
                    {{ student.admin.first_name }} {{ student.admin.last_name }} ({{ student.course_id.course_name }})
                </label>
            </div>
            {% endfor %}
            {% if not students %}
                <p style="color: var(--text-muted);">No students available.</p>
            {% endif %}
        </div>
        
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Save Attendance</button>
    </form>
</div>
{% endblock %}
"""

staff_view_attendance_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Attendance History</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Subject</th>
            <th>Date</th>
        </tr>
        {% for att in attendances %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ att.subject_id.subject_name }}</td>
            <td>{{ att.attendance_date }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

student_view_attendance_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>My Attendance</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Date</th>
            <th>Subject</th>
            <th>Status</th>
        </tr>
        {% for rep in reports %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ rep.attendance_id.attendance_date }}</td>
            <td>{{ rep.attendance_id.subject_id.subject_name }}</td>
            <td>
                {% if rep.status %} <span style="color: var(--success);">Present</span> 
                {% else %} <span style="color: var(--danger);">Absent</span> {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\profile.html", "w") as f: f.write(profile_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\take_attendance.html", "w") as f: f.write(take_attendance_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\view_attendance.html", "w") as f: f.write(staff_view_attendance_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\student_template\view_attendance.html", "w") as f: f.write(student_view_attendance_html)

print("Final features generated.")
