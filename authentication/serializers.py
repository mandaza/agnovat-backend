from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that uses email instead of username"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add email field and remove username field
        self.fields['email'] = serializers.EmailField(help_text='Enter your email address')
        del self.fields['username']
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Find user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('No user found with this email address.')
            
            # Check password
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid email or password.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            # Get token using parent class method
            refresh = self.get_token(user)
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            raise serializers.ValidationError('Must include email and password.')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, help_text="Current password")
    new_password = serializers.CharField(required=True, min_length=8, help_text="New password (minimum 8 characters)")
    
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value