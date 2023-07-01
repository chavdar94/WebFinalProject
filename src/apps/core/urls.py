from django.urls import path, include
from django.contrib.auth import views as auth_views

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

    # password reset urls
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
