from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserCreds
from .forms import UserSignupForm, TherapistSignupForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Therapist, ChatRoom, CallRequest, ChatMessage

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
                request.session['name'] = user.first_name
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
    name = request.session.get('name')  # Retrieve first name from session

    if not user_id:
        return redirect('login')

    context = {'name': name}  # Pass the name to the template

    if role == 'user':
        return render(request, 'mha/dashboard_user.html', context)
    elif role == 'therapist':
        return render(request, 'mha/dashboard_therapist.html', context)
    else:
        return redirect('login')
    
# Logout View
def logout_view(request):
    request.session.flush()  # Clear session
    return redirect('login')



def therapist_list(request):
    therapists = Therapist.objects.all()
    return render(request, "mha/therapist_list.html", {"therapists": therapists})

@login_required
def therapist_detail(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    return render(request, "therapist_detail.html", {"therapist": therapist})

@login_required
def start_chat(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    chat_room, created = ChatRoom.objects.get_or_create(user=request.user, therapist=therapist)
    return redirect("chat_room", room_id=chat_room.id)

@login_required
def send_message(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, id=room_id)
        message = request.POST["message"]
        ChatMessage.objects.create(room=room, sender=request.user, message=message)
    return redirect("chat_room", room_id=room_id)

@login_required
def call_request(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    CallRequest.objects.create(user=request.user, therapist=therapist, status="pending")
    return redirect("therapist_detail", therapist_id=therapist.id)

@login_required
def handle_call_request(request, request_id, action):
    call_request = get_object_or_404(CallRequest, id=request_id)
    if action == "accept":
        call_request.status = "accepted"
    elif action == "reject":
        call_request.status = "rejected"
    call_request.save()
    return redirect("therapist_dashboard")

