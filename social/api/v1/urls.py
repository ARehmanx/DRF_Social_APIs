from django.urls import re_path

from social.api.v1.viewsets import (
    GoogleLogin,
    AppleLogin,
    FacebookLogin,
)


urlpatterns = [
    re_path(r'^login/google/$', GoogleLogin.as_view(), name='google_login'),
    re_path(r'^login/apple/$', AppleLogin.as_view(), name='apple_login'),
    re_path(r'^login/facebook/$', FacebookLogin.as_view(), name='facebook_login'),
]
