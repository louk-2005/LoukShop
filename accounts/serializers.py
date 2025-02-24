#django files
from django.utils.translation import gettext_lazy as _

#rest_frame files
from rest_framework import serializers

#your files
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'password1')
        extra_kwargs = {
            'password': {'write_only': True},
        }


    def validate_email(self, value):
        user = User.objects.filter(email=value).exists()
        if user:
            raise serializers.ValidationError(_('User with this email already exists'))
        return value

    def validate_phone(self, value):
        user = User.objects.filter(phone=value)
        if user:
            raise serializers.ValidationError(_('User with this phone already exists'))
        return value
    def validate(self, data):
        if data['password1'] != data['password']:
            raise serializers.ValidationError({'password':str( _('Passwords do not match'))})
        return data
    def create(self, validated_data):
        del validated_data['password1']
        user = User.objects.create_user(**validated_data)
        return user
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
        write_only=True,
        error_messages={'invalid argument': _('Password must be at least 8 characters long with at least one capital letter and symbol' )}
    )
    password1 = serializers.CharField(write_only=True, required=True)
    def validate(self, data):
        if data['password1'] != data['password']:
            raise serializers.ValidationError({'password': str(_('Passwords do not match'))})
        return data



