from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email

from . import models


class CustomUserRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)

    def get_cleaned_data(self):
        super(CustomUserRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user


class CustomUserLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class CustomUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUserProfile
        fields = ('patronymic', 'gender', 'avatar', 'phone',)


class CustomUserSerializer(serializers.ModelSerializer):
    profile = CustomUserProfileSerializer()

    class Meta:
        model = models.CustomUser
        fields = (
            'email', 'first_name', 'last_name', 'date_of_birth', 'profile')
        read_only_fields = ('email',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.date_of_birth = validated_data.get('date_of_birth',
                                                    instance.date_of_birth)

        profile.patronymic = profile_data.get('patronymic', profile.patronymic)
        profile.gender = profile_data.get('gender',
                                          profile.gender)
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.phone = profile_data.get('phone', profile.phone)
        instance.save()

        return instance


class CustomUserListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api:customuser-detail',
        lookup_field='pk',
    )

    class Meta:
        model = models.CustomUser
        fields = (
            'url', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)