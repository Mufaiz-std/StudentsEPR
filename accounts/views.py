import os
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CustomUser

logger = logging.getLogger(__name__)


def login_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect('admin_home')
        elif request.user.user_type == 2:
            return redirect('staff_home')
        elif request.user.user_type == 3:
            return redirect('student_home')
    return render(request, 'accounts/login.html')


def do_login(request):
    if request.method != 'POST':
        return redirect('login_page')

    user_name = request.POST.get('username')
    user_pass = request.POST.get('password')
    user = authenticate(request, username=user_name, password=user_pass)
    if user is not None:
        login(request, user)
        if user.user_type == 1:
            return redirect('admin_home')
        elif user.user_type == 2:
            return redirect('staff_home')
        elif user.user_type == 3:
            return redirect('student_home')
        return redirect('login_page')

    messages.error(request, 'Invalid login details')
    return redirect('login_page')


def logout_user(request):
    logout(request)
    return redirect('login_page')


@login_required(login_url='/')
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        user.first_name = first_name
        user.last_name = last_name
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile_view')

    return render(request, 'accounts/profile.html', {'user': user})
