from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from user.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(ModelSerializer):
    email =serializers.EmailField(max_length=60)
    password = serializers.CharField( min_length=8, write_only=True)
    class Meta:
        model = User
        
        fields=['email','username','password']
        
        
    def validate(self,attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('Email has already been used')
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        password = validated_data.pop("password")
        
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user