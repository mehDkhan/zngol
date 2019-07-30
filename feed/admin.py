from django.contrib import admin
from .models import Post,Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author')
    list_filter = ('created','author')
    search_fields = ['title','body']
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    ordering = ('created','updated')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','author','created')
    list_filter = ('created','author')
    search_fields = ['body']
    raw_id_fields = ('author','post')
    ordering = ('created',)