from rest_framework import serializers
from .models import DriverProfile, FoundItem, LostItem, User
from django.contrib.auth import authenticate


class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ('license_plate', 'vehicle_type', 'vehicle_description')
        extra_kwargs = {
            'user': {'read_only': True}
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    driver_profile = DriverProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone_number', 'location', 'role', 'password', 'driver_profile')

    def create(self, validated_data):
        driver_data = validated_data.pop('driver_profile', None)
        user = User.objects.create_user(**validated_data)
        
        if user.role == 'driver' and driver_data:
            DriverProfile.objects.create(user=user, **driver_data)
        
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone_number', 'location', 'role')


class LostItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostItem
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']

class FoundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundItem
        fields = '__all__'
        read_only_fields = ['user', 'timestamp']