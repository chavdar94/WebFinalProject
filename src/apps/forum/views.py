from django.shortcuts import render

from django.views import generic as views
from .models import Post, Topic, Comment


class ForumPage(views.ListView):
    model = Post
    template_name = 'forum/forum.html'
    paginate_by = 10


class AllTopicsView(views.ListView):
    model = Topic
    template_name = 'forum/posts.html'


class TopicPage(views.ListView):
    model = Post
    template_name = 'forum/topic.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(topic_id__name=self.kwargs['name'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        topic_name = Topic.objects.filter(name=self.kwargs['name']).get()
        context['topic'] = topic_name
        return context


class PostDetailsPage(views.View):
    def get(self, request, slug):
        post = Post.objects.filter(slug=slug).get()
        comments = post.comment_set.all()

        context = {
            'post': post,
            'comments': comments,
        }

        return render(request, 'forum/post-details.html', context)
