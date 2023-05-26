from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins, get_user_model, authenticate, login
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist

from .forms import ProfileUpdateForm, RegisterForm, SignInForm, PasswordChangeForm
from .models import UserProfile
from ..forum import models as forum_models

UserModel = get_user_model()


class HomePage(views.ListView):
    template_name = 'account/home.html'
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

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             'Invalid form, please enter valid email and password.')
        return redirect('sign-up')


class SignIn(SuccessMessageMixin, auth_views.LoginView):
    form_class = SignInForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    success_message = 'You logged in successfully.'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             'Invalid email or password, please enter valid email and password.')
        return redirect('sign-in')


class SignOut(SuccessMessageMixin, auth_views.LogoutView):
    pass


def signup_redirect(request):
    messages.error(
        request, "Something wrong here, it may be that you already have account!")
    return redirect('sign-in')


class ProfileView(views.View):
    template_name = 'profile/profile.html'

    def get(self, request, pk):
        user = UserModel.objects.filter(pk=pk).get()
        # profile = UserProfile.objects.filter(user_id=user.pk).get()

        try:
            profile = UserProfile.objects.filter(user_id=user.pk).get()
        except ObjectDoesNotExist:
            profile = UserProfile.objects.create(user=user)

        context = {
            'profile': profile,
            'user': user,
        }

        return render(request, self.template_name, context)


class ProfileEditView(auth_mixins.LoginRequiredMixin, views.View):

    def post(self, request, pk):
        user = UserModel.objects.filter(pk=pk).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()

        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('profile-page', pk=pk)

    def get(self, request, pk):
        user = UserModel.objects.filter(pk=pk).get()
        profile = UserProfile.objects.filter(user_id=user.pk).get()

        form = ProfileUpdateForm(instance=profile)

        context = {
            'form': form
        }

        return render(request, 'profile/profile-edit.html', context)


class PasswordChangeView(auth_mixins.LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'profile/password-reset.html'

    def get_success_url(self) -> str:
        user_pk = self.kwargs['pk']
        return reverse_lazy('profile-page', kwargs={'pk': user_pk})

    def get_object(self):
        id_ = self.kwargs['pk']
        return get_object_or_404(UserModel, id_)


class ProfileDeleteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = UserModel
    success_url = reverse_lazy('home')
    template_name = 'profile/delete-profile.html'
