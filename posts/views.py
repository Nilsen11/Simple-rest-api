from rest_framework import generics
from .models import Post
from .serializers import PostSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class BasePostAttr(object):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer


class PostList(BasePostAttr, generics.ListAPIView, generics.CreateAPIView):

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.http_method_names = ['get']
        return Post.objects.all()

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)


class PostDetail(BasePostAttr, generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        queryset = Post.objects.all()

        if not queryset.filter(user=self.request.user, id=self.kwargs["pk"]):
            self.http_method_names = ['get']
        return queryset


class PostListLike(BasePostAttr, generics.ListAPIView, generics.CreateAPIView):

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.http_method_names = ['get']

        return Post.objects.filter(title__icontains=self.kwargs["title"])

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)


class PostListUnLike(BasePostAttr, generics.ListAPIView, generics.CreateAPIView):

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.http_method_names = ['get']

        return Post.objects.exclude(title__icontains=self.kwargs["title"])

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)
