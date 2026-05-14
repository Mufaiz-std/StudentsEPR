import os
import re

views_code = """
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

"""

# Append views
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    content = f.read()

content = re.sub(r"@login_required\(login_url='/'\)\ndef manage_course\(request\):\n    return render\(request, 'admin_template/manage_course\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef manage_subject\(request\):\n    return render\(request, 'admin_template/manage_subject\.html'\)", "", content)

with open(views_path, 'w') as f:
    f.write(content + "\n" + views_code)


urls_code = """
    path('add_course_save/', views.add_course_save, name="add_course_save"),
    path('add_subject_save/', views.add_subject_save, name="add_subject_save"),
"""

urls_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\urls.py"
with open(urls_path, 'r') as f:
    ucontent = f.read()

if "add_course_save" not in ucontent:
    ucontent = ucontent.replace("]", urls_code + "\n]")
    with open(urls_path, 'w') as f:
        f.write(ucontent)

# Templates
course_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Add New Course</h2>
    <form action="{% url 'add_course_save' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <input type="text" name="course_name" placeholder="Course Name" required class="form-input">
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Add Course</button>
    </form>
</div>
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Course List</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">ID</th><th>Course Name</th>
        </tr>
        {% for course in courses %}
        <tr style="border-bottom: 1px solid var(--border-color);"><td style="padding: 10px;">{{ course.id }}</td><td>{{ course.course_name }}</td></tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

subject_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Add New Subject</h2>
    <form action="{% url 'add_subject_save' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <input type="text" name="subject_name" placeholder="Subject Name" required class="form-input" style="margin-bottom: 15px;">
        <select name="course_id" required class="form-input" style="margin-bottom: 15px;">
            {% for course in courses %}<option value="{{ course.id }}">{{ course.course_name }}</option>{% endfor %}
        </select>
        <select name="staff_id" required class="form-input">
            {% for staff in staffs %}<option value="{{ staff.id }}">{{ staff.first_name }} {{ staff.last_name }}</option>{% endfor %}
        </select>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Add Subject</button>
    </form>
</div>
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Subject List</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Subject</th><th>Course</th><th>Staff</th>
        </tr>
        {% for subject in subjects %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ subject.subject_name }}</td><td>{{ subject.course_id.course_name }}</td><td>{{ subject.staff_id.first_name }} {{ subject.staff_id.last_name }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\manage_course.html", "w") as f: f.write(course_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\manage_subject.html", "w") as f: f.write(subject_html)

print("Course and Subject Configurations Completed.")
