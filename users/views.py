from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import PrivateUserSerializer


class Me(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user

        serializer = PrivateUserSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors)

        user = serializer.save()

        serializer = PrivateUserSerializer(user)

        return Response(serializer.data)


class Users(APIView):

    def post(self, request):

        password = request.data["password"]

        if not password:
            raise ParseError

        serializer = PrivateUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        """
        .set_password()는 User 객체에 존재하는 메소드이기 때문에
        유저를 생성하고, 패스워드를 저장해 주어야 한다.  
        """
        user = serializer.save()

        user.set_password(password)
        user.save()

        return Response(serializer.data)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

        serializer = PrivateUserSerializer(user)

        return Response(serializer.data)


class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            user = request.user
            old_password = request.data["old_password"]
            new_password = request.data["new_password"]

        except KeyError:
            raise ParseError("Need password")

        if not user.check_password(old_password):
            raise ParseError("Old password is wrong")

        user.set_password(new_password)
        user.save()

        return Response(status=status.HTTP_200_OK)


class LogIn(APIView):

    def post(self, request):
        try:
            username = request.data["username"]
            password = request.data["password"]

        except KeyError:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if not user:
            return Response({"error": "wrong password"})

        login(request, user)
        return Response({"OK": "Welcome!"})


class LogOut(APIView):

    permission_classes = IsAuthenticated

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye"})
