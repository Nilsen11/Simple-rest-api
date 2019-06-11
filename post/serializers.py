from rest_framework import serializers
from core import models
from django.contrib.auth import get_user_model


class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        fields = ('id', 'user', 'title', 'content', 'created_at', 'updated_at',)
        model = models.Post
