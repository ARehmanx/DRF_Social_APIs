import requests
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.apple.views import AppleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from home.api.v1.serializers import UserSerializer
from social.api.v1.serializers import (
    AppleSocialLoginSerializer,
)


def save_image_from_url(model, url, name):
    r = requests.get(url)
    if r.status_code == 200:
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()
        model.name = name
        model.profile_picture.save("{}.jpg".format(model.username), File(img_temp), save=True)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    serializer_class = SocialLoginSerializer
    client_class = OAuth2Client
    permission_classes = [AllowAny, ]
    callback_url = "https://developers.google.com/oauthplayground"

    def get_response(self):
        serializer_class = self.get_response_serializer()
        user = self.user
        user_extra_data = SocialAccount.objects.filter(user=self.request.user,
                                                       provider__contains='google').first().extra_data
        name = user_extra_data["name"]
        profile_image_url = user_extra_data["picture"]
        if not user.profile_picture:
            save_image_from_url(user, profile_image_url, name)
        user_detail = UserSerializer(user, many=False, context={"request": self.request})
        serializer = serializer_class(instance=self.token, context={'request': self.request})
        resp = serializer.data
        resp["token"] = resp["key"]
        resp.pop("key")
        resp["user"] = user_detail.data
        response = Response(resp, status=status.HTTP_200_OK)
        return response


class AppleLogin(SocialLoginView):
    authentication_classes = []
    permission_classes = [AllowAny]
    adapter_class = AppleOAuth2Adapter
    serializer_class = AppleSocialLoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()
        user = self.user
        user_detail = UserSerializer(user, many=False, context={'request': self.request})
        serializer = serializer_class(instance=self.token, context={'request': self.request})
        resp = serializer.data
        resp["token"] = resp["key"]
        resp.pop("key")
        resp["user"] = user_detail.data
        return Response(resp, status=status.HTTP_200_OK)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    permission_classes = [AllowAny, ]

    def get_response(self):
        serializer_class = self.get_response_serializer()
        user = self.user
        user_extra_data = SocialAccount.objects.filter(user=self.request.user,
                                                       provider__contains='facebook').first().extra_data
        name = user_extra_data["name"]
        if not user.profile_picture:
            profile_image_url = user_extra_data["picture"]["data"]["url"]
            save_image_from_url(user, profile_image_url, name)
        user_detail = UserSerializer(user, many=False)
        serializer = serializer_class(instance=self.token, context={'request': self.request})
        resp = serializer.data
        resp["token"] = resp["key"]
        resp.pop("key")
        resp["user"] = user_detail.data
        return Response(resp, status=status.HTTP_200_OK)
