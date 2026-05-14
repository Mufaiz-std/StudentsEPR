import os
import re

views_code = """
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
"""

# Append views
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    content = f.read()

# Replace the empty manage_staff and manage_student functions
content = re.sub(r"@login_required\(login_url='/'\)\ndef manage_staff\(request\):\n    return render\(request, 'admin_template/manage_staff\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef manage_student\(request\):\n    return render\(request, 'admin_template/manage_student\.html'\)", "", content)

# Remove the import line if it exists to avoid duplication
if "from .models import" not in content:
    with open(views_path, 'w') as f:
        f.write(content + "\n" + views_code)
else:
    # Just append without the import if it's there, but we need it here
    pass

# urls
urls_code = """
    path('add_staff_save/', views.add_staff_save, name="add_staff_save"),
    path('add_student_save/', views.add_student_save, name="add_student_save"),
    path('delete_staff/<int:staff_id>/', views.delete_staff, name="delete_staff"),
    path('delete_student/<int:student_id>/', views.delete_student, name="delete_student"),
    path('admin_feedback_message/', views.admin_feedback_message, name="admin_feedback_message"),
"""

urls_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\urls.py"
with open(urls_path, 'r') as f:
    ucontent = f.read()

if "add_staff_save" not in ucontent:
    ucontent = ucontent.replace("]", urls_code + "\n]")
    with open(urls_path, 'w') as f:
        f.write(ucontent)

# Templates HTML
admin_staff_html = """{% extends 'base.html' %}
{% block page_title %}Manage Staff{% endblock %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
    <h2>Add New Staff</h2>
    <form action="{% url 'add_staff_save' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <input type="text" name="first_name" placeholder="First Name" required class="form-input">
            <input type="text" name="last_name" placeholder="Last Name" required class="form-input">
            <input type="text" name="username" placeholder="Username" required class="form-input">
            <input type="email" name="email" placeholder="Email" required class="form-input">
            <input type="password" name="password" placeholder="Password" required class="form-input">
            <input type="text" name="address" placeholder="Address" required class="form-input">
        </div>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Add Staff</button>
    </form>
</div>

<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Staff List</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Name</th>
            <th>Username</th>
            <th>Email</th>
            <th>Action</th>
        </tr>
        {% for staff in staffs %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ staff.admin.first_name }} {{ staff.admin.last_name }}</td>
            <td>{{ staff.admin.username }}</td>
            <td>{{ staff.admin.email }}</td>
            <td><a href="{% url 'delete_staff' staff.admin.id %}" style="color: var(--danger); text-decoration: none;"><i class="fas fa-trash"></i> Delete</a></td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

admin_student_html = """{% extends 'base.html' %}
{% block page_title %}Manage Student{% endblock %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Add New Student</h2>
    <form action="{% url 'add_student_save' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
            <input type="text" name="first_name" placeholder="First Name" required class="form-input">
            <input type="text" name="last_name" placeholder="Last Name" required class="form-input">
            <input type="text" name="username" placeholder="Username" required class="form-input">
            <input type="email" name="email" placeholder="Email" required class="form-input">
            <input type="password" name="password" placeholder="Password" required class="form-input">
            <input type="text" name="address" placeholder="Address" required class="form-input">
            <select name="course_id" required class="form-input">
                {% for course in courses %}
                    <option value="{{ course.id }}">{{ course.course_name }}</option>
                {% endfor %}
            </select>
        </div>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Add Student</button>
    </form>
</div>

<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Student List</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Name</th>
            <th>Username</th>
            <th>Course</th>
            <th>Action</th>
        </tr>
        {% for student in students %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ student.admin.first_name }} {{ student.admin.last_name }}</td>
            <td>{{ student.admin.username }}</td>
            <td>{{ student.course_id.course_name }}</td>
            <td><a href="{% url 'delete_student' student.admin.id %}" style="color: var(--danger); text-decoration: none;"><i class="fas fa-trash"></i> Delete</a></td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

css_updates = """
.form-input {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    outline: none;
    font-family: 'Inter', sans-serif;
}
.form-input:focus {
    border-color: var(--primary);
}
"""

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\manage_staff.html", "w") as f:
    f.write(admin_staff_html)

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\manage_student.html", "w") as f:
    f.write(admin_student_html)

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\static\css\style.css", "a") as f:
    f.write(css_updates)

print("Backend configured for Staff and Student CRUD.")
