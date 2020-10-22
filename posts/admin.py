from django.contrib import admin

from .models import Comment, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group",)
    search_fields = ("text", )
    list_filter = ("pub_date", )
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    search_fields = ("title", )
    prepopulated_fields = {"slug": ("title", )}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "pub_date", "author",)
    search_fields = ("text", "author",)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment)
