from rest_framework import generics
from core.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class IsUser(BasePermission):
    """
    Allows access only to users.
    """

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_staff)


class CreatePost(generics.CreateAPIView):
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated, IsUser,)

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)


class UserPosts(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(user__username=self.kwargs['username'])
        return queryset


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user, id=self.kwargs["pk"])

        if self.request.user.is_superuser:
            queryset = Post.objects.filter(id=self.kwargs["pk"])

        return queryset


class PostList(generics.ListAPIView):
    """Class that show all posts for authenticated users"""
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.all()


class PostListLike(PostList):
    """Class that show all "posts like" for authenticated users"""

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.kwargs["title"])


class PostListUnLike(PostList):
    """Class that show all "posts unlike" for authenticated users"""

    def get_queryset(self):
        return Post.objects.exclude(title__icontains=self.kwargs["title"])
