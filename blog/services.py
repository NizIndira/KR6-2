from blog.models import Blog
from django.conf import settings
from django.core.cache import cache


def get_blog_cache():
    """ Настройка низкоуровневого кеширования для списка статей блога """

    if settings.CACHE_ENABLED:
        cache_key = 'blog_list'
        blog_list = cache.get(cache_key)
        if blog_list is None:
            category_list = Blog.objects.all()
            cache.set(cache_key, category_list, 60)
    else:
        blog_list = Blog.objects.all()
    return blog_list
