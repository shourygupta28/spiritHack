from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationFormTeacher, UserRegistrationFormStudent, UserRegistrationFormCompany
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import User
User = get_user_model()



def studentregister(request):
    if request.method == 'POST':
        form = UserRegistrationFormStudent(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_student = True

            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')

    else:
        form = UserRegistrationFormStudent()
    return render(request, 'user/register_student.html', {'form': form})

def teacherregister(request):
    if request.method == 'POST':
        form = UserRegistrationFormTeacher(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_teacher = True

            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')

    else:
        form = UserRegistrationFormTeacher()
    return render(request, 'user/register_teacher.html', {'form': form})

def companyregister(request):
    if request.method == 'POST':
        form = UserRegistrationFormCompany(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_company = True

            messages.success(request, f'Your account has been created! You can login now.')
            return redirect('login')

    else:
        form = UserRegistrationFormTeacher()
    return render(request, 'user/register_company.html', {'form': form})

