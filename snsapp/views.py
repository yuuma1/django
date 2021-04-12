from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from thread.models import Topic
from django.utils import timezone



def top(request):
    ctx = {'title': '集まれ司法書士'}
    return render(request, 'app1/top.html', ctx)

def todo(request):
    return render(request, 'app1/todo.html')

class TopView(TemplateView):
    template_name = 'app1/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = '集まれ司法書士'
        return ctx


class TopicListView(ListView):
    template_name = 'app1/top.html'
    # model = Topic
    queryset = Topic.objects.order_by('-created')
    context_object_name = 'topic_list'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.new_list = []

    def get_queryset(self):
        topic_list = Topic.objects.order_by('-created')
        self.new_list = self._make_new_list(topic_list)
        return topic_list

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['new_list'] = self.new_list
        return ctx

    def _make_new_list(self, topic_list):
        def pickup_topic(topic):
            now = timezone.now()
            diff = (now - topic.created).total_seconds() / (60 * 60)
            if diff > 1:
                return False
            else:
                return True
        return list(map(lambda x : x.id ,filter(pickup_topic, topic_list)))
