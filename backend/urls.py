from django.contrib import admin
from django.urls import path, include
from authentication.views import manage_custom_users, manage_verification_tokens  # Import the new Django views
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),  # Ensure this is correct
    path('api/', include('ecommerce.urls')),
    path('admin/custom_users/', manage_custom_users, name='manage_custom_users'),  # Add the custom admin routes
    path('admin/verification_tokens/', manage_verification_tokens, name='manage_verification_tokens'),  # Add the custom admin routes
    path('auth/', include('social_django.urls', namespace='social')),
    path('', TemplateView.as_view(template_name='index.html')),
]
