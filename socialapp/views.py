from rest_framework import viewsets
from rest_framework.response import Response
from .models import Post, LikeDislike, Tag
from .serializers import PostSerializer, LikeDislikeSerializer, TagSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import PostSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination


@permission_classes([IsAuthenticated])
class PostViewSet(viewsets.ModelViewSet):
    def list(self, request):
        page_size = 2
        queryset = Post.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(
            result_page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

    def create(self, request):
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LikeDislikeViewSet(viewsets.ViewSet):
    queryset = LikeDislike.objects.all()
    def list(self, request):
        serializer = LikeDislikeSerializer(self.queryset, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ViewSet):
    queryset = Tag.objects.all()

    def list(self, request):
        serializer = TagSerializer(self.queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    like_obj, created = LikeDislike.objects.get_or_create(
        user=request.user, post=post)
    like_obj.liked = True
    like_obj.save()
    return Response({'status': 'liked'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    like_obj, created = LikeDislike.objects.get_or_create(
        user=request.user, post=post)
    like_obj.liked = False
    like_obj.save()
    return Response({'status': 'disliked'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_user(request, post_id):
    post = Post.objects.get(pk=post_id)
    obj = LikeDislike.objects.filter(
        post=post, liked=True).values_list('user_id', flat=True)
    user_obj = User.objects.filter(id__in=obj).values()
    return Response(user_obj, status=status.HTTP_200_OK)
