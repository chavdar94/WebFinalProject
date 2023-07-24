from datetime import timedelta
from urllib.parse import urlencode

from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model, authenticate, login
from django.contrib.auth import views as auth_views, logout
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .forms import ProfileUpdateForm, RegisterForm, SignInForm, PasswordChangeForm
from .models import UserProfile
from ..forum import models as forum_models
from ..forum.models import Comment, Post

UserModel = get_user_model()


class HomePage(views.ListView):
    template_name = 'base/home.html'
    model = forum_models.Post

    def get_queryset(self):
        return forum_models.Post.objects.all()[:3]


class SignUp(SuccessMessageMixin, auth_mixins.UserPassesTestMixin, views.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('sign-in')
    template_name = 'account/sign-up.html'
    success_message = f'Account successfully created. You are now logged in.'

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('home')

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get(
            'email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)

        return valid


class SignIn(auth_views.LoginView):
    form_class = SignInForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.clear()
            self.request.session.set_expiry(0)

        return super().form_valid(form)

    def form_invalid(self, form):
        form.errors.clear()
        form.add_error(None, 'Invalid email or password')
        return super().form_invalid(form)


class SignOut(auth_mixins.LoginRequiredMixin, views.View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You logged out successfully')
        return redirect('home')


def signup_redirect(request):
    messages.error(
        request, "Something wrong here, it may be that you already have account!")
    return redirect('sign-in')


class ProfileView(views.View):
    template_name = 'profile/profile.html'

    def get(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        user_comments = Comment.objects.select_related(
            'author').filter(author=user)

        paginator = Paginator(user_comments, 8)
        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        user_posts = Post.objects.select_related(
            'author').filter(author=user)[:4]

        try:
            profile = UserProfile.objects.filter(user_id=user.pk).get()
        except ObjectDoesNotExist:
            profile = UserProfile.objects.create(user=user)
	print(profile.profile_picture)

        context = {
            'profile': profile,
            'user': user,
            'user_comments': user_comments,
            'user_posts': user_posts,
            'paginator': paginator,
            'page_number': page_number,
            'page_obj': page_obj,
        }

        return render(request, self.template_name, context)


class ProfileEditView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.View):

    def post(self, request, *args, **kwargs):
        user = UserModel.objects.filter(pk=self.kwargs['pk']).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()

        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            obj = form.save(commit=False)
            pp = form.cleaned_data.get('profile_picture')
            obj.profile_picture = pp
            obj.save()

            return redirect('profile-page', pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        user = UserModel.objects.filter(pk=self.kwargs['pk']).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()

        form = ProfileUpdateForm(instance=profile)

        context = {
            'form': form,
            'user': user,
        }

        return render(request, 'profile/profile-edit.html', context)

    def test_func(self):
        return self.get_object().pk == self.request.user.pk or self.request.user.is_superuser \
            or self.request.user.is_staff

    def handle_no_permission(self):
        raise Http404()

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(UserModel, pk=pk)
        return obj


class PasswordChangeView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin,
                         auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'profile/password-reset.html'

    def get_success_url(self):
        user_pk = self.kwargs['pk']
        return reverse_lazy('profile-page', kwargs={'pk': user_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(UserModel, pk=pk)
        return obj

    def test_func(self):
        return self.get_object().pk == self.request.user.pk or self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404()


class ProfileDeleteView(auth_mixins.UserPassesTestMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = UserModel
    success_url = reverse_lazy('home')
    template_name = 'profile/delete-profile.html'

    def test_func(self):
        return self.get_object().pk == self.request.user.pk or self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404()


# http error views

def bad_request(request, exception):
    context = {}
    return render(request, '404.html', context, status=400)


def permission_denied(request, exception):
    context = {}
    return render(request, '404.html', context, status=403)


def server_error(request):
    context = {}
    return render(request, '404.html', context, status=500)
