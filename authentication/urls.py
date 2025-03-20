from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/google/', views.google_login, name='google_login'),
    path('auth/facebook/', views.facebook_login, name='facebook_login'),
    path('auth/verify-email/<str:token>/', views.verify_email, name='verify_email'),
    path('auth/resend-verification/', views.resend_verification, name='resend_verification'),
    path('auth/profile/', views.get_user_profile, name='profile'),
    path('auth/profile/update/', views.update_user_profile, name='update-profile'),  # Ensure this matches the function name in views.py
    path('auth/forgot-password/', views.forgot_password, name='forgot-password'),
    path('auth/reset-password/', views.reset_password, name='reset-password'),
    path('auth/logout/', views.logout_view, name='logout'),
]
