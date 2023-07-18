from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('sign-in/', views.SignIn.as_view(), name='sign-in'),
    path('sign-out/', views.SignOut.as_view(), name='sign-out'),
    path('accounts/google/login/', views.signup_redirect, name='signup_redirect'),
    path('profile/', include([
        path('<int:pk>/', views.ProfileView.as_view(), name='profile-page'),
        path('<int:pk>/edit-profile',
             views.ProfileEditView.as_view(), name='profile-edit'),
        path('<int:pk>/change-password/',
             views.PasswordChangeView.as_view(), name='password-change'),
        path('<int:pk>/delete-account/',
             views.ProfileDeleteView.as_view(), name='delete-account'),
    ])),


]
