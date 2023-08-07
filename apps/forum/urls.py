from django.urls import path, include

from .post import views as post_views
from .topic import views as topic_views

urlpatterns = [
    path('', topic_views.ForumPage.as_view(), name='forum_page'),

    # topics
    path('topics/', topic_views.AllTopicsView.as_view(), name='forum_topics'),
    path('topics/<str:slug>/', topic_views.TopicPage.as_view(), name='topic_page'),
    path('topics/<str:slug>/delete/',
         topic_views.TopicDelete.as_view(), name='topic_delete'),
    path('create/topics/', topic_views.TopicCreate.as_view(), name='topic_create'),

    # posts
    path('post/<str:slug>/', include([
        path('', post_views.PostDetailsPage.as_view(), name='post_details'),
        path('like/', post_views.post_like, name='post_like'),
        path('create/', post_views.PostCreateView.as_view(), name='post_create'),
        path('edit/', post_views.PostEditView.as_view(), name='post_edit'),
        path('delete/', post_views.PostDeleteView.as_view(), name='post_delete'),
        path('comment/<int:pk>/edit/',
             post_views.CommentEditView.as_view(), name='comment_edit'),
        path('comment/<int:pk>/delete/',
             post_views.CommentDeleteView.as_view(), name='comment_delete'),
    ])),
    path('comment/<int:pk>/', post_views.comment_like, name='comment_like'),
]
