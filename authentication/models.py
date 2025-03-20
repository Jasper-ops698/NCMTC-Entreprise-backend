from mongoengine import Document, StringField, EmailField, BooleanField, ImageField, DecimalField, DateTimeField, ReferenceField, CASCADE
from django.utils.translation import gettext_lazy as _
from datetime import datetime

class CustomUser(Document):
    email = EmailField(required=True, unique=True)
    phone = StringField(max_length=15, blank=True, null=True)
    profile_picture = StringField(blank=True, null=True)  # Use StringField for storing image URLs
    email_verified = BooleanField(default=False)
    is_seller = BooleanField(default=False)
    business_name = StringField(max_length=100, blank=True, null=True)
    business_description = StringField(blank=True, null=True)

    meta = {
        'collection': 'custom_user',  # MongoDB collection name
        'indexes': ['email'],  # Index for faster lookups
    }

    def __str__(self):
        return self.email


class VerificationToken(Document):
    user = ReferenceField(CustomUser, reverse_delete_rule=CASCADE)
    token = StringField(max_length=255, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    expires_at = DateTimeField(required=True)
    type = StringField(max_length=20, choices=['email', 'password'], required=True)

    meta = {
        'collection': 'verification_token',  # MongoDB collection name
        'indexes': [
            'token',
            ('user', 'type'),  # Compound index for user and type
        ],
    }

    def __str__(self):
        return f"{self.type} token for {self.user.email}"


class Service(Document):
    user = ReferenceField(CustomUser, reverse_delete_rule=CASCADE)
    title = StringField(max_length=255, required=True)
    description = StringField(required=True)
    price = DecimalField(precision=2, required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'service',  # MongoDB collection name
        'indexes': ['title'],  # Index for faster lookups
    }

    def __str__(self):
        return self.title
