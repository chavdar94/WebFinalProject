from django.shortcuts import render

from django.views import generic as views
from .models import Post, Topic


class Forum(views.ListView):
    model = Topic
    template_name = 'forum/posts.html'


class TopicPage(views.ListView):
    model = Post
    template_name = 'forum/topic.html'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(topic_id__name=self.kwargs['name'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        topic_name = Topic.objects.filter(name=self.kwargs['name']).get()
        context['topic'] = topic_name
        return context
