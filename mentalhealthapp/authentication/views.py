from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.http import JsonResponse
import json
from .models import UserCreds, Therapist, ChatRoom, CallRequest, ChatMessage, GAD7Response
from .forms import UserSignupForm, TherapistSignupForm
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import MoodEntry
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserCreds
from .forms import UserSignupForm, TherapistSignupForm
from .forms import JournalEntryForm
from django.contrib.auth.decorators import login_required
from .models import JournalEntry
from django.db import connection
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.utils.timezone import localtime

# User Signup View
def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'user'
            user.password = make_password(user.password)
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
            user.password = make_password(user.password)
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

# Dashboard View
def dashboard(request):
    user_id = request.session.get('user_id')
    role = request.session.get('role')
    name = request.session.get('name')

    if not user_id:
        return redirect('login')

    context = {'name': name}
    if role == 'user':
        return render(request, 'mha/dashboard_user.html', context)
    elif role == 'therapist':
        return render(request, 'mha/dashboard_therapist.html', context)
    return redirect('login')

# Logout View
def logout_view(request):
    request.session.flush()
    return redirect('login')

# Therapist List
def therapist_list(request):
    therapists = Therapist.objects.all()
    return render(request, "mha/therapist_list.html", {"therapists": therapists})

# Therapist Details
@login_required
def therapist_detail(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    return render(request, "mha/therapist_detail.html", {"therapist": therapist})

# Start Chat
@login_required
def start_chat(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    chat_room, created = ChatRoom.objects.get_or_create(user=request.user, therapist=therapist)
    return redirect("chat_room", room_id=chat_room.id)

# Send Message
@login_required
def send_message(request, room_id):
    if request.method == "POST":
        room = get_object_or_404(ChatRoom, id=room_id)
        message = request.POST["message"]
        ChatMessage.objects.create(room=room, sender=request.user, message=message)
    return redirect("chat_room", room_id=room_id)

# Call Request
@login_required
def call_request(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    CallRequest.objects.create(user=request.user, therapist=therapist, status="pending")
    return redirect("therapist_detail", therapist_id=therapist.id)

# Handle Call Request
@login_required
def handle_call_request(request, request_id, action):
    call_request = get_object_or_404(CallRequest, id=request_id)
    if action == "accept":
        call_request.status = "accepted"
    elif action == "reject":
        call_request.status = "rejected"
    call_request.save()
    return redirect("therapist_dashboard")

# Intelligence & Personality Tests
def intelligence_test(request):
    return render(request, 'mha/intelligence_test.html')

def personality_test(request):
    return render(request, 'mha/personality_test.html')

def logical_math_test(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responses = data.get("responses", [])
        total_score = sum(responses)
        percentage = (total_score / 25) * 100
        recommendation = (
            "You have strong Logical-Mathematical intelligence!" if percentage >= 80 else
            "You have moderate Logical-Mathematical intelligence." if percentage >= 50 else
            "Consider improving Logical-Mathematical skills through practice."
        )
        return JsonResponse({"score": total_score, "percentage": percentage, "recommendation": recommendation})
    return render(request, 'mha/logical_math_test.html')

def linguistic_test(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responses = data.get("responses", [])
        percentage = (sum(responses) / (5 * len(responses))) * 100
        recommendation = (
            "Excellent linguistic skills! Consider writing or public speaking." if percentage >= 80 else
            "Good language skills. Keep improving through reading and writing!" if percentage >= 50 else
            "Try engaging in vocabulary-building activities."
        )
        return JsonResponse({"percentage": percentage, "recommendation": recommendation})
    return render(request, "mha/linguistic_test.html")

# GAD-7 Test

def GAD_7(request):
    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "You must be logged in to take the test.")
            return redirect("login")

        try:
            total_score = sum(int(request.POST.get(f"q{i}", 0)) for i in range(1, 8))
            GAD7Response.objects.create(user=user, total_score=total_score)
            messages.success(request, "Test submitted successfully!")
            return redirect("progress_report")
        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

    return render(request, 'mha/GAD_7.html')

# PTSD Test
def PTSD(request):
    return render(request, 'mha/PTSD.html')


def spatial_test(request):
     if request.method == "POST":
        data = json.loads(request.body)
        score = sum(data["responses"])
        percentage = (score / 25) * 100  # Max score is 25

        recommendation = "High spatial intelligence! You excel in visualizing and working with spatial information." if percentage > 70 else "You have moderate spatial intelligence."

        return JsonResponse({"percentage": percentage, "recommendation": recommendation})
     return render(request, "mha/spatial_test.html")

def musical_test(request):
    if request.method == "POST":
        data = json.loads(request.body)
        score = sum(data["responses"])
        percentage = (score / 25) * 100  # Max score is 25

        recommendation = "You have strong musical intelligence! Music plays an important role in your learning and creativity." if percentage > 70 else "You have moderate musical intelligence."

        return JsonResponse({"percentage": percentage, "recommendation": recommendation})
    return render(request, "mha/musical_test.html")

def extraversion_test(request):
   if request.method == "POST":
        data = json.loads(request.body)  # Assuming you're using AJAX to send data
        score = sum(data.get("answers", []))  # Sum of Yes (1) answers

        return render(request, "extraversion_result.html", {"score": score})
   return render(request, "mha/extraversion_test.html")

def neuroticism_test(request):
    return render(request, 'mha/neuroticism_test.html')

def psychoticism_test(request):
    return render(request, 'mha/psychoticism_test.html')

def track(request):
    return render(request, 'mha/track.html')





@login_required
def mood_tracker(request):
    if request.method == "POST":
        mood = request.POST.get('mood')
        comment = request.POST.get('comment')

        MoodEntry.objects.create(user=request.user, mood=mood, comment=comment)

        return JsonResponse({'message': 'Mood recorded successfully!'})

    return render(request, 'mood_tracker.html')

@login_required
def mood_history(request):
    moods = MoodEntry.objects.filter(user=request.user).order_by('-date')
    return JsonResponse(list(moods.values('date', 'mood', 'comment')), safe=False)

@login_required
def mood_data(request):
    moods = MoodEntry.objects.filter(user=request.user).values('mood').annotate(count=Count('mood'))
    mood_dict = {mood['mood']: mood['count'] for mood in moods}
    return JsonResponse(mood_dict)


def journal(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    try:
        user = UserCreds.objects.get(id=user_id)
    except UserCreds.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    journal_entry = form.save(commit=False)
                    journal_entry.user = user
                    journal_entry.created_at = localtime(timezone.now())  # Use localtime for IST
                    journal_entry.save()
                    messages.success(request, 'Journal entry saved successfully!')
            except Exception as e:
                messages.error(request, 'Error saving journal entry. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
        return redirect('journal')
    else:
        form = JournalEntryForm()

    journal_entries = JournalEntry.objects.filter(user=user).order_by("-created_at")
    
    return render(request, "mha/journal.html", {
        "journal_entries": journal_entries,
        "form": form,
        "user": user
    })

def delete_journal_entry(request, entry_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    try:
        # Get the entry and verify it belongs to the current user
        entry = JournalEntry.objects.get(id=entry_id, user_id=user_id)
        entry.delete()
        messages.success(request, 'Journal entry deleted successfully!')
    except JournalEntry.DoesNotExist:
        messages.error(request, 'Journal entry not found or you do not have permission to delete it.')
    
    return redirect('journal')