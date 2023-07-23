from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.http import Http404

from .forms import PostCreateForm, CommentCreateForm, PostUpdateForm, PostDeleteForm, CommentEditForm, CommentDeleteForm
from ..models import Post, Topic, Comment


class PostCreateView(auth_mixins.LoginRequiredMixin, views.CreateView):
    form_class = PostCreateForm
    template_name = 'forum/post/post-create.html'
    model = Post

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.topic = Topic.objects.filter(slug=self.kwargs['slug']).get()
        return super().form_valid(form)

    def form_invalid(self, form):
        title = form.instance.title
        if Post.objects.filter(title=title).exists():
            form.errors.clear()
            form.add_error('title',
                           'A post with this title already exists, please try another one or check the existing one.')
            return super().form_invalid(form)

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = Topic.objects.filter(slug=self.kwargs['slug']).get()
        return context


class PostDetailsPage(views.View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comments = post.comment_set.all()

        context = {
            'post': post,
            'comments': comments,
            'form': CommentCreateForm(),
        }

        return render(request, 'forum/post/post-details.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        post = Post.objects.filter(slug=kwargs['slug']).get()

        if form.is_valid():
            data = form.cleaned_data
            data['author'] = request.user
            data['post'] = Post.objects.filter(slug=kwargs['slug']).get()
            comment = Comment(**data)
            comment.save()
            return redirect('post_details', slug=kwargs['slug'])

        context = {
            'form': form,
            'post': post,
        }
        return render(request, 'forum/post/post-details.html', context)


class PostEditView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = PostUpdateForm
    template_name = 'forum/post/post-edit.html'
    queryset = Post.objects.all()

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()


class PostDeleteView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    form_class = PostDeleteForm
    model = Post
    template_name = 'forum/post/post-delete.html'
    success_url = reverse_lazy('forum_page')

    def get_form_kwargs(self):
        instance = self.get_object()
        form = super().get_form_kwargs()
        form.update(instance=instance)
        return form

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()


class CommentEditView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    form_class = CommentEditForm
    template_name = 'forum/post/comment-edit.html'
    model = Comment

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'slug': self.kwargs['slug']})

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()


class CommentDeleteView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    form_class = CommentDeleteForm
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('post_details', kwargs={'slug': self.kwargs['slug']})

    def test_func(self):
        return self.get_object().author.pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()
