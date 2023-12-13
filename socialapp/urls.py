from django.urls import path, include
from .views import like_post, dislike_post, list_user
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('posts', PostViewSet,
                basename='posts')
urlpatterns = [
    path('', include(router.urls)),
    path('like/<int:post_id>/', like_post, name='like-post'),
    path('dislike/<int:post_id>/', dislike_post, name='dislike-post'),
    path('list_user/<int:post_id>/', list_user, name='list_-user'),


]
