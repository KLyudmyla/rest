from django.conf.urls import url
from post.views import *

urlpatterns = (
    url(r'^$', PostList.as_view(), name='posts_list'),
    url(r'^(?P<pk>[0-9]+)/$', PostDetail.as_view(), name='post_detail'),
    url(r'^like/$', LikeList.as_view(), name='post_like'),
)

