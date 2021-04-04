from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from thread.models import Topic


def top(request):
    ctx = {'title': '集まれ司法書士'}
    return render(request, 'app1/top.html', ctx)

class TopView(TemplateView):
    template_name = 'app1/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = '集まれ司法書士'
        return ctx

class TopicListView(ListView):
    template_name = 'app1/top.html'
    queryset = Topic.objects.order_by('-created')
    context_object_name = 'topic_list'