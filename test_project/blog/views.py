from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'You are not authorized to delete this post'}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'You are not authorized to update this post'}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

class PostLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            return Response({'count': post.likes.count()})
        else:
            post.likes.add(request.user)
            return Response({'count': post.likes.count()})
