from .models import Post, Like
from django.contrib.auth.models import User
from .serializers import PostSerializer, LikeSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAuthorOrReadOnly
from rest_framework import permissions

class PostList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """
    View for Post list and creating
    """
    queryset = Post.objects.all().order_by("date")
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetail(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """
    View for Post retrieve, update and delete
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class LikeList(generics.GenericAPIView, mixins.CreateModelMixin):
    """
    View for Like creating
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def post(self, request, *args, **kwargs):
        post_id = request.data.get("post_id", -1)
        
        # Check if post_id is valid
        if post_id == "" or len(Post.objects.filter(id = post_id)) == 0:
            return Response(data={"message":"Invalid post_id"}, status=status.HTTP_400_BAD_REQUEST)

        user_id = User.objects.get(username=request.user).id

        # Check if user already liked this post
        if len(Like.objects.filter(post_id=post_id, user_id=user_id)) > 0:
            return Response(data={"message":"Already liking this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the like
        return self.create(request, *args, **kwargs)
