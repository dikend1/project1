from django.core.serializers import serialize
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,permissions
from .models import Like,Comment,Post
from .serializers import PostSerializer,LikeSerializer,CommentSerializers
from django.shortcuts import get_object_or_404


# post
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return None


# Comments
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def comment_created(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    serializer = CommentSerializers(post,data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user,post=post)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# likes
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def like_create(request,post_id):
    post = get_object_or_404(Post,pk=post_id)

    if Like.objects.filter(post=post,user=request.user).exists():
        return Response(
            {"detail":"You already liked this post"},
            status=status.HTTP_400_BAD_REQUEST
        )

    like = Like.objects.create(post=post,user=request.user)
    serialer = LikeSerializer(like)
    return Response(serialer.data,status=status.HTTP_201_CREATED)
