from rest_framework import generics, authentication, permissions
from .serializers import UserSerializer

from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authentication user"""
        return self.request.user


class UserList(generics.ListCreateAPIView):
    """Show users for admin"""
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser,)

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
