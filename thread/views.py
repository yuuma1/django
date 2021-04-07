from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, FormView, DetailView, TemplateView, ListView
from django.urls import reverse_lazy
from . forms import TopicModelForm, TopicForm, CommentModelForm, LoginedUserTopicModelForm, LoginedUserCommentModelForm
from . models import Topic, Category, Comment
from django.db.models import Count
from django.core.mail import send_mail, EmailMessage    
from django.template.loader import get_template

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
    form_class = LoginedUserTopicModelForm
    model = Topic
    success_url = reverse_lazy('snsapp:top')

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return LoginedUserTopicModelForm
        else:
            return TopicModelForm

    def form_valid(self, form):
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            ctx['category'] = form.cleaned_data['category']
            return render(self.request, 'thread/confirm_topic.html', ctx)
        elif self.request.POST.get('next', '') == 'back':
            return render(self.request, 'thread/create_topic.html', ctx)
        elif self.request.POST.get('next', '') == 'create':
            form.save(self.request.user)
            template = get_template('thread/mail/topic_mail.html')
            user_name = self.request.user.username if self.request.user else form.cleaned_data['user_name']
            mail_ctx={
                'title': form.cleaned_data['title'],
                'user_name': user_name,
                'message': form.cleaned_data['message'],
            }
            EmailMessage(
                subject='トピック作成: ' + form.cleaned_data['title'],
                body=template.render(mail_ctx),
                from_email='hogehoge@example.com',
                to=['admin@example.com'],
                cc=['admin2@example.com'],
                bcc=['admin3@example.com'],
            ).send()
            return redirect(self.success_url)
        else:
            return redirect(reverse_lazy('snsapp:top'))

class TopicAndCommentView(FormView):
    template_name = 'thread/detail_topic.html'
    form_class = LoginedUserCommentModelForm

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return LoginedUserCommentModelForm
        else:
            return CommentModelForm

    def form_valid(self, form):
        kwargs = {}
        if self.request.user.is_authenticated:
            kwargs['user'] = self.request.user

        form.save_with_topic(self.kwargs.get('pk'), **kwargs)
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('thread:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(topic_id=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('no')
        return ctx


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

    
    