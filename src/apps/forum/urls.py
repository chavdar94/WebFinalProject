from django.urls import path

from . import views

urlpatterns = [
    path('', views.ForumPage.as_view(), name='forum_page'),
    path('topics/', views.AllTopicsView.as_view(), name='forum_topics'),
    path('topics/<str:name>/', views.TopicPage.as_view(), name='topic_page'),
    path('post/<str:slug>/', views.PostDetailsPage.as_view(), name='post_details'),
]
