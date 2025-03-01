from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import auth
from .models import UserProfile

def signup(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  # "patient" or "therapist"
        
        # Create Firebase User
        user = auth.create_user(email=email, password=password)
        
        # Save user role in database
        UserProfile.objects.create(uid=user.uid, email=email, role=role)
        
        return JsonResponse({"message": "User created successfully", "uid": user.uid})

def login(request):
    if request.method == "POST":
        data = request.POST
        email = data.get("email")
        password = data.get("password")

        # Authenticate User in Firebase
        user = auth.get_user_by_email(email)
        return JsonResponse({"message": "Login successful", "uid": user.uid})

