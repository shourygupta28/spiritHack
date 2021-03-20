from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import User
User = get_user_model()



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email.find("thapar.edu") == -1:
                messages.add_message(request, messages.INFO, f'''Please enter thapar's email id''')
                return redirect('register')
                    
            else:
                User = form.save()
                return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})