from rest_framework import generics
from core.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class PostList(generics.ListAPIView, generics.CreateAPIView):
    """Class that show all posts for authenticated users"""
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def override_allowed_method(self):
        if self.request.user.is_superuser:
            self.http_method_names = ['get', 'options']

    def get_queryset(self):
        self.override_allowed_method()

        return Post.objects.all()

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)


class PostListLike(PostList, generics.ListAPIView, generics.CreateAPIView):
    """Class that show all "posts like" for authenticated users"""

    def get_queryset(self):
        self.override_allowed_method()

        return Post.objects.filter(title__icontains=self.kwargs["title"])


class PostListUnLike(PostList, generics.ListAPIView, generics.CreateAPIView):
    """Class that show all "posts unlike" for authenticated users"""

    def get_queryset(self):
        self.override_allowed_method()

        return Post.objects.exclude(title__icontains=self.kwargs["title"])


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Post.objects.all()

        if not queryset.filter(user=self.request.user, id=self.kwargs["pk"]) or self.request.user.is_superuser:
            self.http_method_names = ['get', 'options']
        return queryset
