from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

from django.conf.urls import url, include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/users/', include('users.urls')),
    url(r'^api/v1/posts/', include('post.urls')),
    url(r'^bot/', include('bot.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url('api-auth/', include('rest_framework.urls')),
    url('rest-auth/', include('rest_auth.urls')),
    url('api/v1/registration/', include('rest_auth.registration.urls')),
]

ROOT_URL = r'^admin/'
