from django.urls import path
from django.shortcuts import redirect
from . import views

# Function to redirect root URL to login page
def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    
    path('', redirect_to_login),  # Redirect root URL to login page
     path('signup/user/', views.user_signup, name='user_signup'),
    path('signup/therapist/', views.therapist_signup, name='therapist_signup'),
    path('login/', views.login_view, name='login'),  # Ensure this matches
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),  
]
