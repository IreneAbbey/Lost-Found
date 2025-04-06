from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, DriverForm
from .models import User, Driver

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        driver_form = DriverForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            if user.role == 'driver' and driver_form.is_valid():
                driver = driver_form.save(commit=False)
                driver.user = user
                driver.save()

            return redirect('login')
    else:
        form = UserRegistrationForm()
        driver_form = DriverForm()

    return render(request, 'accounts/register.html', {'form': form, 'driver_form': driver_form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})

    return render(request, 'accounts/login.html')
