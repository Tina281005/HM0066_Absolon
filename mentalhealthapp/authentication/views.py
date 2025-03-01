from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserCreds
from .forms import UserSignupForm, TherapistSignupForm

# User Signup View
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.password = make_password(user.password)  # Hash password
            user.save()
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'mha/signup.html', {'form': form, 'role': 'User'})

# Therapist Signup View
def therapist_signup(request):
    if request.method == 'POST':
        form = TherapistSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'therapist'
            user.password = make_password(user.password)  # Hash password
            user.save()
            return redirect('login')
    else:
        form = TherapistSignupForm()
    return render(request, 'mha/signup.html', {'form': form, 'role': 'Therapist'})

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = UserCreds.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['role'] = user.role
                return redirect('dashboard')
            else:
                return render(request, 'mha/login.html', {'error': 'Invalid password'})
        except UserCreds.DoesNotExist:
            return render(request, 'mha/login.html', {'error': 'User does not exist'})

    return render(request, 'mha/login.html')

# Dashboard (Redirects based on role)
def dashboard(request):
    user_id = request.session.get('user_id')
    role = request.session.get('role')

    if not user_id:
        return redirect('login')

    if role == 'user':
        return render(request, 'mha/dashboard_user.html')
    elif role == 'therapist':
        return render(request, 'mha/dashboard_therapist.html')
    else:
        return redirect('login')

# Logout View
def logout_view(request):
    request.session.flush()  # Clear session
    return redirect('login')
