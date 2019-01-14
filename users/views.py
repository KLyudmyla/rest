from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.serializers import UserSerializer, UserSerializerGet, UserSerializernew

from rest_framework import generics

from rest_framework import permissions
from rest_auth.registration.views import RegisterView
from pyhunter import PyHunter
from django.conf import settings
from .models import UserProfile
import logging
import clearbit

logger = logging.getLogger(__name__)


class UserList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializernew

    @permission_classes((permissions.AllowAny,))
    def get(self, request, *args, **kwargs):
        """
        List all tasks.
        """
        queryset = UserProfile.objects.all()
        serializer = UserSerializerGet(queryset, many=True)
        return Response(serializer.data)

    @permission_classes((permissions.IsAuthenticated,))
    def post(self, request, *args, **kwargs):
        """
        Create a new task.
        """
        data = request.data.copy()
        data['user'] = self.request.user.id
        serializer = UserSerializernew(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializernew

    @permission_classes((permissions.IsAuthenticated,))
    def delete(self, request, *args, **kwargs):
        user_profile = self.get_object()
        UserProfile.objects.get(title=user_profile.title).delete()
        user_profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserRegister(RegisterView):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # emailhunter.co for verifying email existence on signup
        user_email = serializer.data['email']
        hunter = PyHunter(settings.HUNTER_KEY)
        if hunter.email_verifier(user_email)['result'] == 'undeliverable':
            logger.warning('New user with invalid email was registered. Email: %s' % user_email)
            # I let the user with the undeliverable email to register because we have to implement bot for this task,
            # otherwise we would have here:
            # return Response(
            #    {'message': 'New user with invalid email tried to register. Email: %s' % user_email},
            #      status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                clearbit.key = settings.CLEARBIT_KEY
                person = clearbit.Person.find(email=user_email, stream=True)
            except:
                person = None
            if person:
                full_name = person['name']['fullName']
                country = person['geo']['country']
            else:
                full_name = None
                country = None
            user = self.perform_create(serializer)
            user_profile = UserProfile(user=user,
                                       full_name=full_name,
                                       country=country)
            user_profile.save()
            headers = self.get_success_headers(serializer.data)
            logger.info('New user with email %s has been registered' % user_email)
            return Response(self.get_response_data(user),
                            status=status.HTTP_201_CREATED,
                            headers=headers)
