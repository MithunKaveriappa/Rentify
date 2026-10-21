from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# REGISTER
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validation
        if not all([first_name, last_name, email, username, password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'signup.html')

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'signup.html')

        User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password
        )
        messages.success(request, 'Registration Successful! Please sign in.')
        return redirect('signin')
    return render(request, 'signup.html')


# LOGIN
def signin(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', '')
        )
        if user:
            login(request, user)
            messages.success(request, 'Login Successful')
            return redirect('profile_view')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'signin.html')


# PROFILE
@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


# UPDATE PROFILE
@login_required(login_url='signin')
def update_profile(request):
    if request.method == 'POST':
        current_user = request.user
        current_user.first_name = request.POST.get('first_name', '')
        current_user.last_name = request.POST.get('last_name', '')
        current_user.email = request.POST.get('email', '')
        current_user.username = request.POST.get('username', '')
        current_user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    return render(request, 'update_profile.html', {'user': request.user})


# UPDATE PASSWORD
@login_required(login_url='signin')
def update_password(request):
    if request.method == 'POST':
        current_user = request.user
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not current_user.check_password(old_password):
            messages.error(request, 'Invalid old password.')
        elif new_password == old_password:
            messages.error(request, 'New password must be different from old password.')
        elif new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'New password must be at least 8 characters.')
        else:
            current_user.set_password(new_password)
            current_user.save()
            update_session_auth_hash(request, current_user)
            messages.success(request, 'Password updated successfully!')
            return redirect('profile')
    return render(request, 'update_password.html')


# LOGOUT
@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('signin')