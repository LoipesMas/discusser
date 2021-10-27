from rest_framework import serializers
from .models import Post, Like

class PostSerializer(serializers.Serializer):
    """
    Serializer for Post model
    """
    id = serializers.ReadOnlyField()
    date = serializers.ReadOnlyField()
    content = serializers.CharField()
    author = serializers.ReadOnlyField(source="get_author")
    likes = serializers.ReadOnlyField(source="get_likes", default=0)

    def create(self, validated_data):
        post = Post()
        post.content = validated_data['content']

        # Try to get user from request
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        post.author = user

        post.save()
        return post

    def update(self, instance, validated_data):
        # Update only content
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class LikeSerializer(serializers.Serializer):
    """
    Serializer for Like model
    """
    id = serializers.ReadOnlyField()
    user = serializers.ReadOnlyField(source="user.username")
    post_id = serializers.IntegerField()

    def create(self, validated_data):
        like = Like()

        # Get post
        post_id = validated_data.get('post_id')
        like.post = Post.objects.get(id = post_id)

        # Get user from request
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            like.user = user

        like.save()
        return like
