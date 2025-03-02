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
    path("therapist_list/", views.therapist_list, name="therapist_list"),
    path("therapist/<int:therapist_id>/", views.therapist_detail, name="therapist_detail"),
    path("chat/<int:therapist_id>/", views.start_chat, name="start_chat"),
    path("chat_room/<int:room_id>/", views.send_message, name="chat_room"),
    path("call/<int:therapist_id>/", views.call_request, name="call_request"),
    path("call_request/<int:request_id>/<str:action>/", views.handle_call_request, name="handle_call_request"),

    path('intelligence_test/', views.intelligence_test, name='intelligence_test'),
    path('personality_test/', views.personality_test, name='personality_test'),
    path('logical_math_test/', views.logical_math_test, name='logical_math_test'),
    path('linguistic_test/', views.linguistic_test, name='linguistic_test'),
    path('spatial_test/', views.spatial_test, name='spatial_test'),
    path('musical_test/', views.musical_test, name='musical_test'),

    path('extraversion_test/', views.extraversion_test, name='extraversion_test'),
    path('neuroticism_test/', views.neuroticism_test, name='neuroticism_test'),
    path('psychoticism_test/', views.psychoticism_test, name='psychoticism_test'),

    path('track/', views.track, name='track'),
    path('GAD_7/', views.GAD_7, name='GAD_7'),
    path('PTSD/', views.PTSD, name='PTSD'),

]



   

