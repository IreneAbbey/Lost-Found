# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework.authentication import authenticate

# from api.models import FoundItem, LostItem

# User = get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         return User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
    
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(username=data['username'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid username or password.")
#         return user
    
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'phone_number', 'role']

# class LostItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LostItem
#         fields = '__all__'
#         extra_kwargs = {'user': {'required': False}}

# class FoundItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoundItem
#         fields = '__all__'