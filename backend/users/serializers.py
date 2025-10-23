from rest_framework import serializers 
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta: 
        model = User 
        fields = ['id', 'email', 'name', 'password', 'role', 'picture', 'date_joined', 'is_active', 'is_staff']
        read_only_fields = ['id', 'date_joined']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Criptografa a senha
        user.save()
        return user
