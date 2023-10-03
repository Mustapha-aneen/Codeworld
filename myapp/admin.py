from django.contrib import admin
from .models import Post ,Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
  list_display = ("title","slug","publish","image")
  list_filter = ("title","slug","publish","image")
  search_fields = ("title","description")
  prepopulated_fields = {"slug":("title",)}
# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ("name","post","publish","active")
  list_filter = ("name","post","publish","active")