from django.conf.urls import url
from users.views import *
from rest_auth.registration.views import RegisterView

urlpatterns = (
    url(r'^$', UserList.as_view(), name='users_list'),
    url(r'^(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),
    url(r'^registration/$', UserRegister.as_view(), name='rest_register'),
)
