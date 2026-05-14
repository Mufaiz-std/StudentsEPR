import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_erp.settings')
django.setup()

from erp_app.models import CustomUser, Course

def delete_all():
    CustomUser.objects.exclude(is_superuser=True).delete()
    Course.objects.all().delete()
    print("All dummy data deleted successfully.")

if __name__ == "__main__":
    delete_all()
