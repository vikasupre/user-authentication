from rest_framework import serializers
from .models import User,EmailVerificationToken
from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    phone=PhoneNumberField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=('id','email','phone','password','confirm_password')
    
    
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user

class EmailVerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        models=EmailVerificationToken
        fields='__all__'
