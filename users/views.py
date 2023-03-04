from django.contrib.auth import authenticate, login, logout

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
        user = authenticate(request, username=username, password=password)
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
