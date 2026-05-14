import os

templates = {
    'admin_template/manage_staff.html': ('Manage Staff', 'admin_home', 'Add, Edit, and Remove Staff members.'),
    'admin_template/manage_student.html': ('Manage Student', 'admin_home', 'Add, Edit, and Remove Students.'),
    'admin_template/manage_course.html': ('Manage Course', 'admin_home', 'Add, Edit, and Remove Courses.'),
    'admin_template/manage_subject.html': ('Manage Subject', 'admin_home', 'Add, Edit, and Remove Subjects.'),
    
    'staff_template/take_attendance.html': ('Take Attendance', 'staff_home', 'Select subject and mark student attendance.'),
    'staff_template/apply_leave.html': ('Apply Leave', 'staff_home', 'Submit a leave request for Admin approval.'),
    'staff_template/feedback.html': ('Send Feedback', 'staff_home', 'Send feedback or issues to the Administrator.'),
    
    'student_template/view_attendance.html': ('View Attendance', 'student_home', 'Review your overall attendance records.'),
    'student_template/apply_leave.html': ('Apply Leave', 'student_home', 'Submit a leave request for Admin approval.'),
    'student_template/feedback.html': ('Send Feedback', 'student_home', 'Send feedback or issues to the Administrator.')
}

base_dir = r"c:\Users\mufai\python practice\new\TD\StudentERP\templates"

for path, (title, active_url, desc) in templates.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # We extend the base template and add a simple card with the title and description
    content = f"""{{% extends 'base.html' %}}

{{% block page_title %}}{title}{{% endblock %}}

{{% block sidebar_menu %}}
    <!-- Re-include the same sidebar menu from the home_content depending on the role. For simplicity, just provide a back to home link or standard menu -->
    <li><a href="{{% url '{active_url}' %}}"><i class="fas fa-home"></i> Back to Home</a></li>
{{% endblock %}}

{{% block content %}}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; border: 1px solid var(--border-color); box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
    <h2>{title}</h2>
    <p style="margin-top: 10px; color: var(--text-muted);">{desc}</p>
    
    <div style="margin-top: 20px; padding: 40px; text-align: center; background: var(--bg-color); border-radius: 8px; border: 1px dashed var(--border-color);">
        <p style="color: var(--text-muted);"><i class="fas fa-tools fa-2x"></i></p>
        <p style="margin-top: 10px;">Form interface will go here.</p>
    </div>
</div>
{{% endblock %}}
"""
    with open(full_path, 'w') as f:
        f.write(content)

print("All templates created.")
