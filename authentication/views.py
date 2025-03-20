from django.shortcuts import render, redirect
from .models import CustomUser, VerificationToken
from django.contrib.auth import authenticate, login as auth_login, logout  # Import logout function

from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, DetailView
from .models import Service
from mongoengine.errors import DoesNotExist
from datetime import datetime, timedelta
from django.core.mail import send_mail  # Import for sending emails
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import logging  # Import logging module

logger = logging.getLogger(__name__)  # Configure logger for this module

class ServiceListCreateView(ListView, CreateView):
    model = Service
    template_name = 'admin/service_list.html'
    # Add any additional methods or attributes as needed

class ServiceDetailView(DetailView):
    model = Service
    template_name = 'admin/service_detail.html'
    # Add any additional methods or attributes as needed

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile')  # Redirect to user profile after login
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})

    return render(request, 'registration/login.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            password = request.POST.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Email and password are required.'}, status=400)

            # Check if the email is already registered (workaround for QuerySet.exists())
            if CustomUser.objects.filter(email=email).first() is not None:
                return JsonResponse({'error': 'Email is already registered.'}, status=400)

            # Create a new CustomUser
            new_user = CustomUser(email=email)
            new_user.set_password(password)  # Ensure the password is hashed
            new_user.save()

            return JsonResponse({'message': 'User registered successfully.'}, status=201)
        except Exception as e:
            logger.error(f"Error during user registration: {str(e)}", exc_info=True)  # Log the error with traceback
            return JsonResponse({'error': 'An internal server error occurred.'}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def manage_custom_users(request):
    # Logic to manage custom users
    return JsonResponse({'message': 'Manage custom users endpoint'})

def google_login(request):
    # Logic for Google login will go here
    return JsonResponse({'message': 'Google login functionality not implemented yet.'})

def facebook_login(request):
    # Logic for Facebook login will go here
    return JsonResponse({'message': 'Facebook login functionality not implemented yet.'})

def manage_verification_tokens(request):
    # Logic to manage verification tokens
    return JsonResponse({'message': 'Manage verification tokens endpoint'})

def verify_email(request, token):
    try:
        verification_token = VerificationToken.objects.get(token=token, type='email')
        if verification_token.expires_at < datetime.utcnow():
            return JsonResponse({'error': 'Token has expired.'}, status=400)

        user = verification_token.user
        user.email_verified = True
        user.save()
        verification_token.delete()
        return JsonResponse({'message': 'Email verified successfully.'})
    except DoesNotExist:
        return JsonResponse({'error': 'Invalid token.'}, status=400)

def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user.email_verified:
                return JsonResponse({'message': 'Email is already verified.'}, status=400)

            # Generate a new verification token
            token = VerificationToken.objects.create(
                user=user,
                token='new_generated_token',  # Replace with actual token generation logic
                type='email',
                expires_at=datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
            )

            # Send verification email
            send_mail(
                'Verify Your Email',
                f'Use this token to verify your email: {token.token}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Verification email resent successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def forgot_password(request):
    """
    Handle forgot password requests by sending a password reset email.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')

        try:
            user = CustomUser.objects.get(email=email)

            # Generate a password reset token
            token = VerificationToken.objects.create(
                user=user,
                token='new_generated_token',  # Replace with actual token generation logic
                type='password_reset',
                expires_at=datetime.utcnow() + timedelta(hours=24)  # Token valid for 24 hours
            )

            # Send password reset email
            send_mail(
                'Reset Your Password',
                f'Use this token to reset your password: {token.token}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Password reset email sent successfully.'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def reset_password(request):
    """
    Handle password reset using a valid token.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        new_password = data.get('new_password')

        try:
            verification_token = VerificationToken.objects.get(token=token, type='password_reset')
            if verification_token.expires_at < datetime.utcnow():
                return JsonResponse({'error': 'Token has expired.'}, status=400)

            user = verification_token.user
            user.set_password(new_password)  # Set the new password
            user.save()
            verification_token.delete()  # Delete the token after successful reset

            return JsonResponse({'message': 'Password reset successfully.'})
        except VerificationToken.DoesNotExist:
            return JsonResponse({'error': 'Invalid token.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def get_user_profile(request):
    """
    Retrieve the profile of the currently logged-in user.
    """
    user = request.user
    profile_data = {
        "username": user.username,
        "email": user.email,
        # Add other user-related fields as needed
    }
    return JsonResponse(profile_data)

@login_required
def update_user_profile(request):
    """
    Update the profile of the currently logged-in user.
    """
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)

        # Update user fields based on the provided data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        # Add other fields as needed

        user.save()
        return JsonResponse({'message': 'Profile updated successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def logout_view(request):
    """
    Log out the currently logged-in user.
    """
    logout(request)
    return JsonResponse({'message': 'Logged out successfully.'})
