from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ForumPage.as_view(), name='forum_page'),
    path('topics/', views.AllTopicsView.as_view(), name='forum_topics'),
    path('topics/<slug:slug>/', views.TopicPage.as_view(), name='topic_page'),
    path('post/<slug:slug>/', include([
        path('', views.PostDetailsPage.as_view(), name='post_details'),
        path('create/', views.PostCreateView.as_view(), name='post_create'),
        path('edit/', views.PostEditView.as_view(), name='post_edit'),
        path('delete/', views.PostDeleteView.as_view(), name='post_delete'),
    ])),
    path('create/topics/', views.TopicCreate.as_view(), name='topic_create'),
]
