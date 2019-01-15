from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from post.serializers import *
from post.models import Post, Like

from rest_framework import permissions
from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import APIView


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method == "GET"


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)

    def get(self, request, *args, **kwargs):
        """
        List all tasks.
        """
        queryset = Post.objects.all()
        serializer = PostSerializerGet(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        data = request.data.copy()
        data['author'] = self.request.user.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @permission_classes((permissions.IsAuthenticated,))
    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        Post.objects.get(title=post.title).delete()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeList(generics.ListCreateAPIView, APIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated|ReadOnly,)

    def get(self, request,  *args, **kwargs):
        """
        List all tasks.
        """
        queryset = Like.objects.all()
        serializer = LikeSerializerGet(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        data = request.data.copy()
        data['user'] = self.request.user.id
        serializer = LikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            likes = Post.objects.get(pk=data['post']).likes
            Post.objects.filter(pk=data['post']).update(likes=likes + 1)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
