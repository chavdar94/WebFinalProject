from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from django.db.models import Q
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.views.generic.edit import FormMixin

from .forms import TopicCreateForm
from ..mixins.moderator_group_mixin import GroupRequiredMixin

from ..models import Post, Topic
from ..post.forms import PostCreateForm


class ForumPage(views.ListView):
    model = Post
    template_name = 'forum/forum.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['pattern'] = self.request.GET.get('pattern', None)
        context['total_posts'] = Post.objects.count()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        pattern = self.__get_pattern()

        if pattern:
            vector = SearchVector('title', 'body', 'topic__name')
            query = SearchQuery(pattern)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).filter(
                rank__gte=0.001).order_by('-rank')

            new_queryset = self.model.objects.filter(
                Q(topic__name__icontains=pattern) |
                Q(body__icontains=pattern) |
                Q(title__icontains=pattern)
            )

            combined_queryset = set(queryset) | set(new_queryset)

            # Convert the combined set back to a queryset
            queryset = self.model.objects.filter(
                pk__in=[obj.pk for obj in combined_queryset])

            return queryset

        return queryset.order_by('-created')

    def __get_pattern(self):
        pattern = self.request.GET.get('pattern', None)
        return pattern.lower() if pattern else None


class AllTopicsView(views.ListView):
    model = Topic
    template_name = 'forum/topics/topic.html'


class TopicPage(FormMixin, views.ListView):
    model = Post
    template_name = 'forum/post/post.html'
    form_class = PostCreateForm
    paginate_by = 8

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(topic_id__slug=self.kwargs['slug']).order_by('-updated')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        topic_name = Topic.objects.filter(slug=self.kwargs['slug']).get()
        context['topic'] = topic_name
        return context

    def get_success_url(self):
        return reverse_lazy('topic_page', kwargs={'slug': self.kwargs['slug']})


class TopicCreate(GroupRequiredMixin, auth_mixins.LoginRequiredMixin, views.CreateView):
    allowed_groups = ['Moderators', 'Admins']
    form_class = TopicCreateForm
    template_name = 'forum/topics/topic-create.html'
    success_url = reverse_lazy('forum_topics')

    def form_valid(self, form):
        if Topic.objects.filter(name=form.cleaned_data['name']).exists():
            form.add_error(
                'name', f'A topic with name ` {form.cleaned_data["name"]} ` already exists, please try another one or '
                        f'check the existing one.')
            return self.form_invalid(form)

        return super().form_valid(form)


class TopicDelete(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin, views.DeleteView):
    model = Topic
    success_url = reverse_lazy('forum_topics')
    template_name = 'forum/topics/topic-delete.html'
    success_url = reverse_lazy('forum_topics')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='Admins').exists()

    def handle_no_permission(self):
        raise Http404()
