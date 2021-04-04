from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView, DetailView, TemplateView, ListView
from django.urls import reverse_lazy
from . forms import TopicCreateForm, TopicModelForm, TopicForm, CommentModelForm
from . models import Topic, Category, Comment

class TopicAndCommentView(FormView):
    template_name = 'thread/detail_topic.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        # comment = form.save(commit=False)
        # comment.topic = Topic.objects.get(id=self.kwargs['pk'])
        # comment.no = Comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        # comment.save()
        form.save_with_topic(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(topic_id=self.kwargs['pk']).order_by('no')
        return ctx

class CategoryView(ListView):
    template_name = 'thread/category.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic.objects.filter(category__url_code = self.kwargs['url_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(Category, url_code=self.kwargs['url_code'])
        return ctx

class TopicCreateView(CreateView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('snsapp:top')

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'thread/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'thread/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('snsapp:top'))

class TopicFormView(FormView):
    template_name = 'thread/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('snsapp:top')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# def topic_create(request):
#     template_name = 'thread/create_topic.html'
#     ctx = {}
#     if request.method == 'GET':
#         ctx['form'] = TopicCreateForm()
#         return render(request, template_name, ctx)
    
#     if request.method == 'POST':
#         topic_form = TopicCreateForm(request.POST)
#         if topic_form.is_valid():
#             topic_form.save()           
#             return redirect(reverse_lazy('snsapp:top'))
#         else:
#             ctx['form'] = topic_form
#             return render(request, template_name, ctx)

class TopicTemplateView(TemplateView):
    template_name = 'thread/detail_topic.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['topic'] = get_object_or_404(Topic, id=self.kwargs.get('pk', ''))
        return ctx

class TopicDetailView(DetailView):
    template_name = 'thread/detail_topic.html'
    model =Topic
    context_object_name = 'topic'

    
    