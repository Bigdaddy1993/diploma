from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'image', 'created_at', 'is_payment', 'views_count', 'owner')
    search_fields = ('title', 'created_at')
