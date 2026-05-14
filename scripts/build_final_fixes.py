import os
import re

# 1. Update Base Template Sidebar
base_html_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\base.html"
with open(base_html_path, 'r') as f:
    base_content = f.read()

sidebar_logic = """
                {% if request.user.user_type == 1 %}
                    <li><a href="{% url 'admin_home' %}"><i class="fas fa-home"></i> Home</a></li>
                    <li><a href="{% url 'manage_staff' %}"><i class="fas fa-users"></i> Staff</a></li>
                    <li><a href="{% url 'manage_student' %}"><i class="fas fa-user-graduate"></i> Students</a></li>
                    <li><a href="{% url 'manage_course' %}"><i class="fas fa-book"></i> Courses</a></li>
                    <li><a href="{% url 'manage_subject' %}"><i class="fas fa-book-open"></i> Subjects</a></li>
                    <li><a href="{% url 'admin_staff_attendance' %}"><i class="fas fa-calendar-check"></i> Staff Attendance</a></li>
                    <li><a href="{% url 'admin_leave_requests' %}"><i class="fas fa-envelope"></i> Leave Requests</a></li>
                    <li><a href="{% url 'admin_feedback_message' %}"><i class="fas fa-comments"></i> Feedback</a></li>
                {% elif request.user.user_type == 2 %}
                    <li><a href="{% url 'staff_home' %}"><i class="fas fa-home"></i> Home</a></li>
                    <li><a href="{% url 'staff_take_attendance' %}"><i class="fas fa-calendar-check"></i> Take Student Attendance</a></li>
                    <li><a href="{% url 'staff_view_attendance' %}"><i class="fas fa-eye"></i> View Student Attendance</a></li>
                    <li><a href="{% url 'staff_view_personal_attendance' %}"><i class="fas fa-eye"></i> My Attendance</a></li>
                    <li><a href="{% url 'staff_student_leave_requests' %}"><i class="fas fa-envelope-open"></i> Student Leaves</a></li>
                    <li><a href="{% url 'staff_apply_leave' %}"><i class="fas fa-envelope"></i> Apply Leave</a></li>
                    <li><a href="{% url 'staff_feedback' %}"><i class="fas fa-comments"></i> Send Feedback</a></li>
                {% elif request.user.user_type == 3 %}
                    <li><a href="{% url 'student_home' %}"><i class="fas fa-home"></i> Home</a></li>
                    <li><a href="{% url 'student_view_attendance' %}"><i class="fas fa-calendar-check"></i> View Attendance</a></li>
                    <li><a href="{% url 'student_apply_leave' %}"><i class="fas fa-envelope"></i> Apply Leave</a></li>
                    <li><a href="{% url 'student_feedback' %}"><i class="fas fa-comments"></i> Send Feedback</a></li>
                {% endif %}
                <li><a href="{% url 'profile_view' %}"><i class="fas fa-user"></i> Profile</a></li>
"""
base_content = re.sub(r"{% block sidebar_menu %}\s*{% endblock %}", sidebar_logic, base_content)
with open(base_html_path, 'w') as f:
    f.write(base_content)


# 2. Remove block sidebar_menu from ALL templates so they use the base one
templates_dir = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates"
for root, dirs, files in os.walk(templates_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            # Regex to remove {% block sidebar_menu %} ... {% endblock %}
            content = re.sub(r"{% block sidebar_menu %}.*?{% endblock %}", "", content, flags=re.DOTALL)
            with open(path, 'w') as f:
                f.write(content)

print("Fixed Sidebar!")
