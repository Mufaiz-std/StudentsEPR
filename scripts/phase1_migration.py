import os
import shutil
import subprocess

base_dir = r"c:\Users\mufai\python practice\new\TD\StudentERP"

# 1. Initialize Apps
apps_to_create = ["accounts", "students", "staff", "management"]
for app in apps_to_create:
    app_path = os.path.join(base_dir, app)
    if not os.path.exists(app_path):
        print(f"Creating app: {app}")
        subprocess.run(["python", "manage.py", "startapp", app], cwd=base_dir)

# 2. Move Templates
# Source directories
src_admin = os.path.join(base_dir, "templates", "admin_template")
src_staff = os.path.join(base_dir, "templates", "staff_template")
src_student = os.path.join(base_dir, "templates", "student_template")

# Destination directories
dest_admin = os.path.join(base_dir, "management", "templates", "management")
dest_staff = os.path.join(base_dir, "staff", "templates", "staff")
dest_student = os.path.join(base_dir, "students", "templates", "students")

# Function to move contents
def move_templates(src, dest):
    if os.path.exists(src):
        os.makedirs(dest, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dest, item)
            shutil.move(s, d)
        print(f"Moved {src} to {dest}")
        # Remove empty source dir
        os.rmdir(src)

move_templates(src_admin, dest_admin)
move_templates(src_staff, dest_staff)
move_templates(src_student, dest_student)

# 3. Setup Static Architecture
static_dirs = [
    "css",
    "js/staff",
    "js/students",
    "js/management",
    "assets"
]

static_base = os.path.join(base_dir, "static")
for d in static_dirs:
    dir_path = os.path.join(static_base, d)
    os.makedirs(dir_path, exist_ok=True)
    print(f"Created static directory: {dir_path}")

print("Phase 1 completed successfully.")
