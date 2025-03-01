from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import auth
from .models import UserProfile

def get_user_role(request, uid):
    try:
        user_profile = UserProfile.objects.get(uid=uid)
        return JsonResponse({"role": user_profile.role})
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

def signup(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  # "patient" or "therapist"

        user = auth.create_user(email=email, password=password)
        UserProfile.objects.create(uid=user.uid, email=email, role=role)
        
        return JsonResponse({"message": "User created successfully", "uid": user.uid})

from django.http import JsonResponse

from django.shortcuts import render
from django.http import JsonResponse

def login(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")

        user = auth.get_user_by_email(email)
        return JsonResponse({"message": "Login successful", "uid": user.uid})

    # Return an HTML login page for GET requests
    return render(request, "mha/login.html")
