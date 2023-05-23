from django.urls import path

from . import views

urlpatterns = [
    path('', views.Forum.as_view(), name='forum_topics'),
    path('topics/<str:name>/', views.TopicPage.as_view(), name='topic_page'),
]
