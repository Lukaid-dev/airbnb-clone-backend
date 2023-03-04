import jwt

from django.conf import settings

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class TrustMeBroAuthentication(BaseAuthentication):
    # BaseAuthentication를 상속받은 모든 class는 authenticate 메소드를 구현해야 함
    def authenticate(self, request):
        # request를 받아서 유저를 반환하는 메소드
        # 유저가 없으면 None을 반환
        # 유저가 있으면 (user, None)을 반환
        # 유저가 있지만 인증에 실패했으면 AuthenticationFailed를 반환
        # 이 메서드의 request에는 user가 없고, 헤너나 쿠키, URL, IP주소 등의 정보가 있음

        username = request.headers.get("Trust-Me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            return AuthenticationFailed(f"User with username: {username} does not exist")


# simple jwt를 쓰자
class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            return AuthenticationFailed("Invalid token")
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            return AuthenticationFailed(f"User with pk: {pk} does not exist")
