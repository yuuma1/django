from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView, DetailView, TemplateView, ListView
from django.urls import reverse_lazy
from . forms import TopicCreateForm, TopicModelForm, TopicForm, CommentModelForm
from . models import Topic, Category, Comment
from django.db.models import Count
     

class TopicAndCommentView(FormView):
    template_name = 'thread/detail_topic.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        # comment = form.save(commit=False)
        # comment.topic = Topic.objects.get(id=self.kwargs['pk'])
        # comment.no = Comment.objects.filter(topic=self.kwargs['pk']).count() + 1
        # comment.save()
        # form.save_with_topic(self.kwargs.get('pk'))
        Comment.objects.create_comment(
            user_name=form.cleaned_data['user_name'],
            message=form.cleaned_data['message'],
            topic_id=self.kwargs['pk'],
            image=form.cleaned_data['image'],
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('thread:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(topic_id=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('no')
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

# class TopicCreateView(CreateView):
#     template_name = 'thread/create_topic.html'
#     form_class = TopicModelForm
#     model = Topic
#     success_url = reverse_lazy('snsapp:top')

#     def form_valid(self, form):
#         ctx = {'form': form}
#         if self.request.POST.get('next', '') == 'confirm':
#             return render(self.request, 'thread/confirm_topic.html', ctx)
#         if self.request.POST.get('next', '') == 'back':
#             return render(self.request, 'thread/create_topic.html', ctx)
#         if self.request.POST.get('next', '') == 'create':
#             return super().form_valid(form)
#         else:
#             return redirect(reverse_lazy('snsapp:top'))


class TocicCreateViewBySession(FormView):
    template_name = 'thread/create_topic.html'
    form_class = TopicModelForm

    def post(self, request, *args, **kwargs):
        ctx = {}
        if request.POST.get('next', '') == 'back':
            if 'input_data' in self.request.session:
                input_data = self.request.session['input_data']
                form = TopicModelForm(input_data)
                ctx['form'] = form
            return render(request, self.template_name, ctx)
        elif request.POST.get('next', '') == 'create':
            if 'input_data' in request.session:
                form = self.form_class(request.session['input_data'])
                form.save()
                request.session.pop('input_data') # セッションに保管した情報の削除
              
                return redirect(reverse_lazy('snsapp:top'))
        elif request.POST.get('next', '') == 'confirm':
            form = TopicModelForm(request.POST)
            if form.is_valid():
                ctx = {'form': form}
                # セッションにデータを保存
                input_data = {
                    'title': form.cleaned_data['title'],
                    'user_name': form.cleaned_data['user_name'],
                    'message': form.cleaned_data['message'],
                    'category': form.cleaned_data['category'].id,
                }
                request.session['input_data'] = input_data
                ctx['category'] = form.cleaned_data['category']
                return render(request, 'thread/confirm_topic.html', ctx)
            else:
                return render(request, self.template_name, {'form': form})


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

    
    