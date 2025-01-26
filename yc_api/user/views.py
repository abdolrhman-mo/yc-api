from rest_framework import status, mixins, viewsets, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from yc_api.permissions import IsAccountOwnerOrAdmin
from .serializers import UserSerializer
from .models import User
from django.contrib.auth import authenticate

class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin):
    """
    A viewset that provides the standard actions.
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwnerOrAdmin]

    def get_permissions(self):
        """
        Customize permissions based on the action.
        """
        if self.action in ['create']:
            self.permission_classes = [permissions.AllowAny]
        elif self.action in ['list']:
            self.permission_classes=[IsAuthenticated]
        elif self.action in ['destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [IsAccountOwnerOrAdmin]
        return super().get_permissions()

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        Log in a user using username and password, and return token and user data.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': 'Invalid username or password'}, status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='test-token', authentication_classes=[TokenAuthentication])
    def test_token(self, request):
        """
        Test view to verify token authentication.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
