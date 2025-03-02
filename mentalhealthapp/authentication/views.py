from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import UserCreds
from .forms import UserSignupForm, TherapistSignupForm
from django.shortcuts import render
from django.http import JsonResponse
import json

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

def intelligence_test(request):
    return render(request, 'mha/intelligence_test.html')

def intelligence_test(request):
    return render(request, 'mha/intelligence_test.html')

def personality_test(request):
    return render(request, 'mha/personality_test.html')

def logical_math_test(request):
    if request.method == "POST":
        data = json.loads(request.body)
        responses = data.get("responses", [])

        total_score = sum(responses)  # Sum of selected values
        max_score = 25  # Maximum possible score
        
        # Calculate percentage score
        percentage = (total_score / max_score) * 100  

        # Recommendations based on the score
        if percentage >= 80:
            recommendation = "You have strong Logical-Mathematical intelligence! Consider careers in engineering, data science, or problem-solving roles."
        elif percentage >= 50:
            recommendation = "You have moderate Logical-Mathematical intelligence. Enhance your skills through puzzles, games, and analytical thinking."
        else:
            recommendation = "You may want to improve Logical-Mathematical intelligence through problem-solving activities."

        return JsonResponse({
            "score": total_score,
            "percentage": percentage,
            "recommendation": recommendation
        })

    return render(request, 'mha/logical_math_test.html')

def linguistic_test(request):
    if request.method == "GET":
        return render(request, "mha/linguistic_test.html")

    elif request.method == "POST":
        data = json.loads(request.body)
        responses = data.get("responses", [])
        percentage = (sum(responses) / (5 * len(responses))) * 100

        recommendation = "Great linguistic skills! Try writing or public speaking." if percentage >= 80 else \
                         "Good language skills. Keep improving by reading and writing!" if percentage >= 50 else \
                         "Try engaging in reading and vocabulary-building activities."

        return JsonResponse({"percentage": percentage, "recommendation": recommendation})

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

from django.contrib import messages

def GAD_7(request):
    if request.method == "POST":
        user = request.user

        # Ensure the user is logged in
        if not user.is_authenticated:
            messages.error(request, "You must be logged in to take the test.")
            return redirect("login")

        try:
            # Get values, default to 0 if missing
            q1 = int(request.POST.get("q1", 0))
            q2 = int(request.POST.get("q2", 0))
            q3 = int(request.POST.get("q3", 0))
            q4 = int(request.POST.get("q4", 0))
            q5 = int(request.POST.get("q5", 0))
            q6 = int(request.POST.get("q6", 0))
            q7 = int(request.POST.get("q7", 0))

            total_score = q1 + q2 + q3 + q4 + q5 + q6 + q7

            # Save to database
            response = GAD7Response.objects.create(
                user=user,
                q1=q1,
                q2=q2,
                q3=q3,
                q4=q4,
                q5=q5,
                q6=q6,
                q7=q7,
                total_score=total_score
            )

            messages.success(request, "Test submitted successfully!")

            return redirect("progress_report")  # Redirect to progress page

        except Exception as e:
            messages.error(request, f"Error saving data: {str(e)}")

    return render(request, 'mha/GAD_7.html')

def PTSD(request):
    return render(request, 'mha/PTSD.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GAD7Response
from django.contrib import messages



@login_required
def progress_report(request):
    user = request.user
    responses = GAD7Response.objects.filter(user=user).order_by("-timestamp")
    return render(request, "mha/progress_report.html", {"responses": responses})