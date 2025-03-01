from django.urls import path
from authentication import views


urlpatterns = [
    path('', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('get-user-role/<str:uid>', views.get_user_role, name="get_user_role"),
]
