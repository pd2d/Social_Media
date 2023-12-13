from rest_framework import serializers
from .models import Tag, Post, PostImage, LikeDislike

#create tag serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

#creating postimage serializer
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'

#creating post serializer
class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    num_likes = serializers.SerializerMethodField()
    num_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('description', 'images', 'tags', 'status',
                  'num_likes', 'num_dislikes', 'created_date')

    def get_images(self, instance):
        obj = PostImage.objects.filter(
            post=instance.id).values_list('image', flat=True)
        return obj

    def get_status(self, post):
        request = self.context['request']
        if request.user.is_authenticated:
            user = request.user
            like_obj = LikeDislike.objects.filter(user=user, post=post).first()
            if like_obj:
                return 'liked' if like_obj.liked else 'disliked'
        return None

    def get_num_likes(self, post):
        return LikeDislike.objects.filter(post=post, liked=True).count()

    def get_num_dislikes(self, post):
        return LikeDislike.objects.filter(post=post, liked=False).count()

#creating LikeDislike serializer
class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'
