from random import random
import jwt
import requests

from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

from users.models import User

from . import serializers


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(data=serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        # password validation
        if not password:
            raise ParseError("Password is required")
        serializer = serializers.PrivateUserSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            user = serializer.save()
            # hash password
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class PublicUser(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(f"User with username: {username} does not exist")
        serializer = serializers.TinyUserSerializer(user)
        return Response(data=serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        if not current_password or not new_password:
            raise ParseError("current_password and new_password are required")
        if not user.check_password(current_password):
            raise ParseError("current_password is wrong")
        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_200_OK)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("username and password are required")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            # serializer = serializers.PrivateUserSerializer(user)
            # return Response(data=serializer.data)
            Response({"message": "Log in success"})
        else:
            Response({"error": "Log in failed"})
            # raise ParseError("username or password is wrong")


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Log out success"})


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("username and password are required")
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            # token은 유저에게 전달되기 떄문에 민감한 정보를 담으면 안됨
            # 유저가 원하면 복호화 가능
            token = jwt.encode(
                {
                    "pk": user.pk,
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            raise ParseError("username or password is wrong")


class GithubLogin(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://github.com/login/oauth/access_token",
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                },
                headers={
                    "Accept": "application/json",
                },
            )
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_data = user_data.json()
            user_emails = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {access_token}",
                },
            )
            user_emails = user_emails.json()
            for email in user_emails:
                if email.get("primary") and email.get("verified"):
                    primary_email = email.get("email")
                    break
            try:
                user = User.objects.get(email=primary_email)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                print("except")
                # 중복 이름이나 이메일 예외처리 하셈
                # if User.objects.get(username=user_data.get("login")):
                #     print("if")
                #     while True:
                #         user_data["login"] = f"{user_data.get('login')}{random.randint(1, 1000)}"
                #         if not User.objects.get(username=user_data.get("login")):
                #             break
                user = User.objects.create(
                    username=user_data.get("login"),
                    email=primary_email,
                    name=user_data.get("name"),
                    avatar=user_data.get("avatar_url"),
                )
                user.set_unusable_password()  # 이 유저는 비밀번호를 사용하지 않음 only login with github
                # user.has_usable_password() 로 확인 가능
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
