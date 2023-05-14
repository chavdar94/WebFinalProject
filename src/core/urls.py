from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up'),
    path('sign-in/', views.SignIn.as_view(), name='sign-in'),
    path('sign-out/', views.SignOut.as_view(), name='sign-out'),
    path('accounts/social/signup/', views.signup_redirect, name='signup_redirect'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile-page'),
    path('profile-edit/<int:pk>',
         views.ProfileEditView.as_view(), name='profile-edit'),
]
