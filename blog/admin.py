from django.contrib import admin
from .models import Post, Category, Tag

class PostInline(admin.TabularInline):
    model = Post
    extra = 3

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [PostInline]

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','created_time','modified_time','category','author']
    list_filter = ['created_time']
    search_fields = ['title']

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
