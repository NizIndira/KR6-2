from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog_view/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
]