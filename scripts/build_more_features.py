import os
import re

views_code = """
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

"""

# Append views
views_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\views.py"
with open(views_path, 'r') as f:
    content = f.read()

# Replace empty functions to avoid duplicates
content = re.sub(r"@login_required\(login_url='/'\)\ndef staff_feedback\(request\):\n    return render\(request, 'staff_template/feedback\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef student_feedback\(request\):\n    return render\(request, 'student_template/feedback\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef staff_apply_leave\(request\):\n    return render\(request, 'staff_template/apply_leave\.html'\)", "", content)
content = re.sub(r"@login_required\(login_url='/'\)\ndef student_apply_leave\(request\):\n    return render\(request, 'student_template/apply_leave\.html'\)", "", content)

with open(views_path, 'w') as f:
    f.write(content + "\n" + views_code)


urls_code = """
    path('staff_feedback_save/', views.staff_feedback_save, name="staff_feedback_save"),
    path('student_feedback_save/', views.student_feedback_save, name="student_feedback_save"),
    path('staff_leave_save/', views.staff_leave_save, name="staff_leave_save"),
    path('student_leave_save/', views.student_leave_save, name="student_leave_save"),
"""

urls_path = r"c:\Users\mufai\python practice\new\TD\StudentERP\erp_app\urls.py"
with open(urls_path, 'r') as f:
    ucontent = f.read()

if "staff_feedback_save" not in ucontent:
    ucontent = ucontent.replace("]", urls_code + "\n]")
    with open(urls_path, 'w') as f:
        f.write(ucontent)

# Templates
feedback_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Send Feedback</h2>
    <form action="{% if request.user.user_type == 2 %}{% url 'staff_feedback_save' %}{% else %}{% url 'student_feedback_save' %}{% endif %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <textarea name="feedback_msg" rows="5" class="form-input" placeholder="Enter your feedback here..." required></textarea>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Submit Feedback</button>
    </form>
</div>

<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Feedback History</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Feedback Message</th>
            <th>Reply</th>
            <th>Date</th>
        </tr>
        {% for fb in feedbacks %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ fb.feedback }}</td>
            <td>{% if fb.feedback_reply %}{{ fb.feedback_reply }}{% else %}<span style="color: var(--warning);">Pending</span>{% endif %}</td>
            <td>{{ fb.created_at|date:"d M Y" }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

leave_html = """{% extends 'base.html' %}
{% block content %}
<div class="content-section" style="background: white; padding: 20px; border-radius: 12px;">
    <h2>Apply for Leave</h2>
    <form action="{% if request.user.user_type == 2 %}{% url 'staff_leave_save' %}{% else %}{% url 'student_leave_save' %}{% endif %}" method="POST" style="margin-top: 15px;">
        {% csrf_token %}
        <input type="date" name="leave_date" class="form-input" required style="margin-bottom: 15px;">
        <textarea name="leave_msg" rows="5" class="form-input" placeholder="Reason for leave..." required></textarea>
        <button type="submit" class="btn-primary" style="margin-top: 15px;">Submit Leave</button>
    </form>
</div>

<div class="content-section" style="background: white; padding: 20px; border-radius: 12px; margin-top: 20px;">
    <h2>Leave History</h2>
    <table style="width: 100%; text-align: left; margin-top: 15px; border-collapse: collapse;">
        <tr style="background: var(--bg-color); border-bottom: 2px solid var(--border-color);">
            <th style="padding: 10px;">Leave Date</th>
            <th>Message</th>
            <th>Status</th>
        </tr>
        {% for leave in leaves %}
        <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 10px;">{{ leave.leave_date }}</td>
            <td>{{ leave.leave_message }}</td>
            <td>
                {% if leave.leave_status == 1 %} <span style="color: var(--success);">Approved</span> 
                {% elif leave.leave_status == 2 %} <span style="color: var(--danger);">Rejected</span> 
                {% else %} <span style="color: var(--warning);">Pending</span> {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</div>
{% endblock %}
"""

with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\feedback.html", "w") as f: f.write(feedback_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\student_template\feedback.html", "w") as f: f.write(feedback_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\staff_template\apply_leave.html", "w") as f: f.write(leave_html)
with open(r"c:\Users\mufai\python practice\new\TD\StudentERP\templates\student_template\apply_leave.html", "w") as f: f.write(leave_html)

print("Feedback and Leave configurations completed.")
