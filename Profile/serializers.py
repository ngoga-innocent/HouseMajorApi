# Profile/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'password', 'account_type']

    def create(self, validated_data):
        validated_data['email'] = validated_data['email'].strip().lower()  # normalize
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email'].strip().lower()  # normalize case
        password = data['password']

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid login credentials")

        data['user'] = user
        return data
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone_number', 'account_type']