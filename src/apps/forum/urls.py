from django.urls import path

from . import views

urlpatterns = [
    path('', views.ForumPage.as_view(), name='forum_page'),
    path('topics/', views.AllTopicsView.as_view(), name='forum_topics'),
    path('topic/<slug:slug>/', views.TopicPage.as_view(), name='topic_page'),
    path('post/<slug:slug>/', views.PostDetailsPage.as_view(), name='post_details'),
    path('create/topic/', views.TopicCreate.as_view(), name='topic_create'),
]
