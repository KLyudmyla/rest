from django.conf.urls import url
from bot.views import *

urlpatterns = (
    url(r'^$', RunBot.as_view(), name='automated_bot'),)
