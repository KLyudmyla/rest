from rest_framework import serializers
from .models import Post, Like
from django.contrib.auth.models import User


class PostSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'author', 'text')


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'text')

    def create(self, validated_data):
        author = User.objects.get(pk=self._kwargs['data']['author'])
        new_post = Post.objects.create(author=author, **validated_data)
        return new_post

    def update(self, instance, validated_data):
        author_data = User.objects.get(pk=self._kwargs['context']['request'].user.id)
        author = instance.author

        author.username = author_data.username
        author.email = author_data.email
        author.save()
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class LikeSerializerGet(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('user', 'post', 'like')


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('post', 'like')

    def create(self, validated_data):
        user = User.objects.get(pk=self._kwargs['data']['user'])
        new_post = Like.objects.create(user=user, **validated_data)
        return new_post
