from django.urls import path, include

from .post import views as post_views
from .topic import views as topic_views

urlpatterns = [
    path('', topic_views.ForumPage.as_view(), name='forum_page'),

    # topics
    path('topics/', topic_views.AllTopicsView.as_view(), name='forum_topics'),
    path('topics/<slug:slug>/', topic_views.TopicPage.as_view(), name='topic_page'),
    path('create/topics/', topic_views.TopicCreate.as_view(), name='topic_create'),

    # posts
    path('post/<slug:slug>/', include([
        path('', post_views.PostDetailsPage.as_view(), name='post_details'),
        path('create/', post_views.PostCreateView.as_view(), name='post_create'),
        path('edit/', post_views.PostEditView.as_view(), name='post_edit'),
        path('delete/', post_views.PostDeleteView.as_view(), name='post_delete'),
    ])),
]
