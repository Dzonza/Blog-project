from django.contrib import admin
from .models import Post, Tag, Comment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    list_filter = ('title', 'author', 'tags',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment)