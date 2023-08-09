from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers


class AuthorizeUserView(CreateAPIView):
    queryset = serializers.User.objects.all()
    serializer_class = serializers.UserSerializer

    def authorize(self, request, user, *args, **kwargs):
        serializer = self.get_serializer(instance=user)
        serializer.send_login_code(user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not "phone_number" in request.data.keys():
            return Response({"phone_number": ["This field is required."]})
        user = self.queryset.filter(phone_number=request.data["phone_number"])
        if user.exists():
            return self.authorize(request, user[0])
        return super().post(request, *args, **kwargs)


class LoginUserView(APIView):
    @swagger_auto_schema(request_body=serializers.LoginSerializer)
    def post(self, request):
        context = {"request": self.request}
        serializer = serializers.LoginSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        return Response("logined")


class ProfileView(RetrieveUpdateAPIView):
    queryset = models.UserProfile.objects.select_related("user").all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "user"

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.get(user=request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.queryset.get(user=request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
