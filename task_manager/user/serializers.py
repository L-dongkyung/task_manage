from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from user.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['last_login', 'is_active', 'is_admin']

    def validate(self, attrs):
        """
        유저 가입시 비밀번호 검증 확인.
        :param attrs:
        :return:
        """
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        del attrs['confirm_password']
        attrs['password'] = make_password(attrs['password'])
        return attrs
