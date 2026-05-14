import os
import re

# 1. Update Home Contents to use dynamic variables
admin_home_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\home_content.html"
with open(admin_home_path, 'r') as f: content = f.read()
content = content.replace("<h3>120</h3>", "<h3>{{ staff_count }}</h3>")
content = content.replace("<h3>450</h3>", "<h3>{{ student_count }}</h3>")
content = content.replace("<h3>15</h3>", "<h3>{{ course_count }}</h3>")
content = content.replace("<h3>42</h3>", "<h3>{{ subject_count }}</h3>")
with open(admin_home_path, 'w') as f: f.write(content)

staff_home_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\home_content.html"
with open(staff_home_path, 'r') as f: content = f.read()
content = content.replace("<h3>120</h3>", "<h3>{{ student_count }}</h3>")
content = content.replace("<h3>4</h3>", "<h3>{{ subject_count }}</h3>")
content = content.replace("<h3>2</h3>", "<h3>{{ leave_count }}</h3>")
with open(staff_home_path, 'w') as f: f.write(content)

student_home_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\student_template\home_content.html"
with open(student_home_path, 'r') as f: content = f.read()
content = content.replace("<h3>85%</h3>", "<h3>{{ attendance_percent }}%</h3>")
content = content.replace("<h3>6</h3>", "<h3>{{ subject_count }}</h3>")
content = content.replace("<h3>1</h3>", "<h3>{{ leave_count }}</h3>")
with open(student_home_path, 'w') as f: f.write(content)


# 2. Admin Staff Attendance Template
admin_staff_att = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Take Staff Attendance</h2>
    <form action="{% url 'admin_staff_attendance' %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <label>Attendance Date</label>
        <input type="date" name="attendance_date" required class="form-input" style="margin-bottom: 15px;">
        
        <h3>Select Staff (Check if Present)</h3>
        <div style="margin-top: 15px; max-height: 300px; overflow-y: auto; border: 1px solid var(--border-color); padding: 10px; border-radius: 6px;">
            {% for staff in staffs %}
            <div style="margin-bottom: 10px;">
                <label>
                    <input type="checkbox" name="staff_ids" value="{{ staff.id }}" style="margin-right: 10px;">
                    {{ staff.admin.first_name }} {{ staff.admin.last_name }}
                </label>
            </div>
            {% endfor %}
        </div>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Save Staff Attendance</button>
    </form>
</div>
{% endblock %}"""
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\staff_attendance.html", "w") as f: f.write(admin_staff_att)


# 3. Staff View Personal Attendance Template
staff_view_personal_att = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>My Attendance</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Date</th>
            <th>Status</th>
        </tr>
        {% for rep in reports %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ rep.attendance_id.attendance_date }}</td>
            <td>
                {% if rep.status %} <span style="color: var(--success);">Present</span> 
                {% else %} <span style="color: var(--danger);">Absent</span> {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}"""
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\view_personal_attendance.html", "w") as f: f.write(staff_view_personal_att)


# 4. Admin Leave Requests Template
admin_leave = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Staff Leave Requests</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Staff</th>
            <th>Date</th>
            <th>Message</th>
            <th>Action</th>
        </tr>
        {% for leave in leaves %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ leave.user.first_name }} {{ leave.user.last_name }}</td>
            <td>{{ leave.leave_date }}</td>
            <td>{{ leave.leave_message }}</td>
            <td>
                {% if leave.leave_status == 0 %}
                    <a href="{% url 'admin_approve_leave' leave.id %}" class="btn-primary" style="padding: 5px 10px; text-decoration: none; font-size: 12px; background: var(--success);">Approve</a>
                    <a href="{% url 'admin_reject_leave' leave.id %}" class="btn-primary" style="padding: 5px 10px; text-decoration: none; font-size: 12px; background: var(--danger);">Reject</a>
                {% elif leave.leave_status == 1 %}
                    <span style="color: var(--success);">Approved</span>
                {% else %}
                    <span style="color: var(--danger);">Rejected</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}"""
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\admin_template\leave_requests.html", "w") as f: f.write(admin_leave)


# 5. Staff Student Leave Requests Template
staff_leave = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Student Leave Requests</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Student</th>
            <th>Date</th>
            <th>Message</th>
            <th>Action</th>
        </tr>
        {% for leave in leaves %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ leave.user.first_name }} {{ leave.user.last_name }}</td>
            <td>{{ leave.leave_date }}</td>
            <td>{{ leave.leave_message }}</td>
            <td>
                {% if leave.leave_status == 0 %}
                    <a href="{% url 'staff_approve_leave' leave.id %}" class="btn-primary" style="padding: 5px 10px; text-decoration: none; font-size: 12px; background: var(--success);">Approve</a>
                    <a href="{% url 'staff_reject_leave' leave.id %}" class="btn-primary" style="padding: 5px 10px; text-decoration: none; font-size: 12px; background: var(--danger);">Reject</a>
                {% elif leave.leave_status == 1 %}
                    <span style="color: var(--success);">Approved</span>
                {% else %}
                    <span style="color: var(--danger);">Rejected</span>
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}"""
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\student_leave_requests.html", "w") as f: f.write(staff_leave)

print("Templates Created.")
