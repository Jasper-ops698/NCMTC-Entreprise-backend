from django.contrib import admin
from .models import CustomUser, VerificationToken

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'email_verified', 'is_seller')
    search_fields = ('email',)
    ordering = ('email',)

class VerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'expires_at', 'type')
    list_filter = ('type', 'created_at')
    search_fields = ('token',)

# Uncomment the following lines if you want to register these models with Django admin
# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(VerificationToken, VerificationTokenAdmin)
