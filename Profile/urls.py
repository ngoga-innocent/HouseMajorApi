# Profile/urls.py
from django.urls import path
from .views import RegisterView, LoginView,forgot_password,get_profile,reset_password,reset_password_form

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', get_profile, name='get_profile'),
    path('forgot-password/',forgot_password),
    
]

