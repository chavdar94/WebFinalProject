from django.shortcuts import render
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank


from django.views import generic as views
from .models import Post, Topic, Comment


class ForumPage(views.ListView):
    model = Post
    template_name = 'forum/forum.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pattern'] = self.request.GET.get('pattern', None)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.__get_pattern()

        if pattern:
            vector = SearchVector('title', 'body', 'topic__name')
            query = SearchQuery(pattern)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.001).order_by('-rank')

        return queryset

    def __get_pattern(self):
        pattern = self.request.GET.get('pattern', None)
        return pattern.lower() if pattern else None


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
