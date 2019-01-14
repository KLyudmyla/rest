from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
import clearbit
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


class UserSerializerGet(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'full_name', 'country')


class UserSerializernew(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ('username', 'email')

    def create(self, validated_data):
        profile_data = validated_data.pop('user')
        user = User.objects.create(**profile_data)
        try:
            clearbit.key = settings.CLEARBIT_KEY
            person = clearbit.Person.find(email=user.email, stream=True)
        except:
            person = None
        if person != None:
            full_name = person['name']['fullName']
            country = person['geo']['country']
        else:
            full_name = None
            country = None
        validated_data.update({full_name: full_name, country: country})
        profile = UserProfile.objects.create(user=user, full_name=full_name, country=country)
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.country = validated_data.get('country', instance.country)
        instance.save()
        return instance
