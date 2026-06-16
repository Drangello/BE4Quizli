from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


def set_auth_cookies(response, refresh):
    """
    Set access and refresh token cookies.
    """
    response.set_cookie(
        "access_token",
        str(refresh.access_token),
        httponly=True,
        samesite="Lax",
    )
    response.set_cookie(
        "refresh_token",
        str(refresh),
        httponly=True,
        samesite="Lax",
    )


class RegisterView(APIView):
    """
    Register a new user.
    """

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User created successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Login user and set auth cookies.
    """

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        response = Response(
            {
                "detail": "Login successfully!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )
        set_auth_cookies(response, refresh)
        return response


class LogoutView(APIView):
    """
    Logout user and blacklist refresh token.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"detail": "Not authenticated."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "detail":
                "Log-Out successfully! All Tokens will be deleted. "
                "Refresh token is now invalid."
            },
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class TokenRefreshCookieView(APIView):
    """
    Refresh access token by refresh cookie.
    """

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh Token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
        except TokenError:
            return Response(
                {"detail": "Refresh Token missing."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {"detail": "Token refreshed"},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            httponly=True,
            samesite="Lax",
        )
        return response
