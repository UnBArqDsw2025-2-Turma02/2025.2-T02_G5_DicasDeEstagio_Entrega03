from rest_framework import serializers 
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User 
        fields = ['id', 'email', 'name', 'password', 'role', 'picture', 'date_joined', 'is_active', 'is_staff']
        read_only_fields = ['id', 'date_joined']
