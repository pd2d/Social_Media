from django.contrib import admin
from .models import Tag, Post, PostImage, LikeDislike
from django.contrib import admin
from nested_admin import NestedModelAdmin, NestedStackedInline

#registering tag and like and dislike with admin.py
admin.site.register(Tag)
admin.site.register(LikeDislike)


class PostImageInline(NestedStackedInline):
    """
    PostImage inline
    """
    model = PostImage
    extra = 0                # No.empty forms to display for adding new PostImage
    can_delete = True        # to delete individual PostImage
    show_change_link = True  # display a change link for each PostImage instance


@admin.register(Post)                 #post module accessible from the admin panel
class PostsAdmin(NestedModelAdmin):   #new admin class named PostsAdmin 
    """
    Admin panel config for Post
    """

    list_display = ('description',)  #show the description of each post
    list_filter = ('tags',)          #adds a filter allowing users to filter Post based on tags 
    inlines = (PostImageInline,)     #included as an inline within the PostsAdmin admin class
