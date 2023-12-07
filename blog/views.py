from django.views.generic import ListView, DetailView

from blog.models import Blog
from blog.services import get_blog_cache


class BlogListView(ListView):
    """Контроллер блога для просмотра списка статей"""

    model = Blog

    def get_context_data(self, **kwargs):
        context = {
            'blog_list': get_blog_cache()
        }

        return context


class BlogDetailView(DetailView):
    """Контроллер блога для детального просмотра статьи"""

    model = Blog

    def get_object(self, queryset=None):
        """Создаем счетчик просмотров"""

        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object
