from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import CustomUser
from .models import Service

class UserSerializer(DocumentSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'profile_picture',
            'email_verified',
            'is_seller',
            'business_name',
            'business_description',
        )
        read_only_fields = ('email_verified',)

class ServiceSerializer(DocumentSerializer):
    class Meta:
        model = Service
        fields = ['id', 'user', 'title', 'description', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
