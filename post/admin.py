from django.contrib import admin
from .models import Post, Like


class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ["title", "author", "likes"]
    search_fields = ["title"]
    list_filter = ["title", "author"]
    save_on_top = True


class LikeAdmin(admin.ModelAdmin):
    model = Like
    list_display = ["like", "post", "user"]
    search_fields = ["post", "user"]
    list_filter = ["post", "user"]
    save_on_top = True


admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
