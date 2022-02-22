from carway_api.permissions import IsSuperuserOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import AuthTokenSerializer, UserCreateSerializer, UserDetailSerializer, UserListSerializer
from rest_framework import parsers, renderers, permissions, generics
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrReadOnly]
    serializer_class = UserCreateSerializer


class UserListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrReadOnly]
    serializer_class = UserListSerializer

    def get_queryset(self):
        """
        This view should return a list of all the users
        for the superuser or the user currwntly authinticated.
        """
        user = self.request.user
        if user and user.is_superuser:
            return CustomUser.objects.all().order_by('-date_joined')
        return CustomUser.objects.filter(email=user)


# ToDo: Change the preission to let the user  to update his own informations.
class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrReadOnly]
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all the users
        for the superuser or the user currwntly authinticated.
        """
        user = self.request.user
        if user and user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(email=user)


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'is_superuser': user.is_superuser})
