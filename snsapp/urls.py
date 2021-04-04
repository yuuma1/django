from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'snsapp'

urlpatterns = [
    path('', views.TopicListView.as_view(), name='top'),
    path('terms/', TemplateView.as_view(template_name='app1/terms.html'), name='terms'),
    path('policy/', TemplateView.as_view(template_name='app1/policy.html'), name='policy'),
    path('about/', TemplateView.as_view(template_name='app1/about.html'), name='about'),
]
