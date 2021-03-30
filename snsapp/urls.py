from django.urls import path
from . import views

app_name = 'snsapp'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post_create', views.post_create, name='post_create'),
]