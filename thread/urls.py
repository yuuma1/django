from django.urls import path

from . import views

app_name = 'thread'

urlpatterns = [
    # path('create_topic/', views.TocicCreateViewBySession.as_view(), name='create_topic'),
    path('create_topic/', views.TopicCreateView.as_view(), name='create_topic'),
    # path('<int:pk>/', views.TopicAndCommentView.as_view(), name='topic'),
    path('<int:pk>/', views.TopicAndCommentView.as_view(), name='topic'),
    # path('category/<str:url_code>/', views.CategoryView.as_view(), name='category'),
    path('category/<str:url_code>/', views.CategoryView.as_view(), name='category'),
    path('<int:pk>/', views.TopicTemplateView.as_view(), name='topic'),
    # path('create_topic/', views.TopicFormView.as_view, name='create_topic'),
    path('<int:pk>/', views.TopicDetailView.as_view(), name='topic'),
]
