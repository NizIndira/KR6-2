from django.contrib import admin
from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    """Представление раздела - блог в админке"""

    list_display = ('title', 'creation_date')
    search_fields = ('title', 'description',)
