from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post
from user.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'text', 'likes']

    def create(self, validated_data):
        user = self.context['request'].user
        likes_data = validated_data.pop('likes', [])
        blog_post = Post.objects.create(user=user, **validated_data)
        for like_data in likes_data:
            blog_post.likes.add(like_data)
        return blog_post