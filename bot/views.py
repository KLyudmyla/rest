from bot.serializers import *
from django.conf import settings
import random
import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import permission_classes

logger = logging.getLogger(__name__)


class RunBot(generics.GenericAPIView):
    serializer_class = BotSerializer

    @permission_classes((permissions.AllowAny,))
    def post(self, request, *args, **kwargs):
        data = {'number_of_users': settings.NUMBER_OF_USERS,
                'number_posts_per_user': random.randint(1, settings.MAX_POSTS_PER_USER),
                'number_likes_per_user': random.randint(1, settings.MAX_LIKES_PER_USER)}
        serializer = BotSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.instance, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
