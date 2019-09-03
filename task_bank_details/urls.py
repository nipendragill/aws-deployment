from django.conf.urls import url
from .views import CreateUserAPIView, authenticate_user

urlpatterns = [
    url(r'^create/$', CreateUserAPIView.as_view(), name='create_user'),
    url(r'^get_token/$', authenticate_user, name='get_token'),
]