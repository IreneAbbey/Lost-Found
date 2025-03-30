from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            password=validated_data['password']
        )
        return user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'password']