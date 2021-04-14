from django import forms
from django.forms import ModelForm
from . models import Topic, Category, Comment

class LoginedUserCommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user_name',
            'message',
            'image',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    def save_with_topic(self, topic_id, user, commit=True, **kwargs):
        comment = self.save(commit=False)
        comment.topic = Topic.objects.get(id=topic_id)
        comment.no = Comment.objects.filter(topic_id=topic_id).count() + 1
        if commit:
            comment.save()
        return comment

class CommentModelForm(forms.ModelForm):
    user_name = forms.CharField(label='名前', required=True,)
    email = forms.EmailField(label='メールアドレス', required=True,)
    class Meta:
        model = Comment
        fields = [
            'user_name',
            'image',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs['value'] = 'ゲストユーザー'

    def save_with_topic(self, topic_id, commit=True, **kwargs):
        comment = self.save(commit=False)
        comment.topic = Topic.objects.get(id=topic_id)
        comment.no = Comment.objects.filter(topic_id=topic_id).count() + 1
        comment.user_name = self.cleaned_data['user_name']
        comment.email = self.cleaned_data['email']
        if commit:
            comment.save()
        return comment

class TopicCreateForm(ModelForm):
    class Meta:
        model=Topic
        fields=[
            'title',
            'user_name',
            'category',
            'image',
            'message',
        ]

class TopicModelForm(forms.ModelForm):
    user_name = forms.CharField(label='ゲストユーザー名', required=True,)
    email = forms.EmailField(label='メールアドレス', required=True,)
    class Meta:
        model=Topic
        fields=[
            'title',
            'category',
            'message',
        ]
        widget = {
            'title' : forms.TextInput(attrs={'class': 'hoge'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '選択して下さい'
        self.fields['user_name'].widget.attrs['value'] = 'ゲストユーザー'

    def save(self, commit=True):
        topic = super().save(commit=False)
        topic.user_name = self.cleaned_data['user_name']
        topic.email = self.cleaned_data['email']
        if commit:
            topic.save()
        return topic

class LoginedUserTopicModelForm(forms.ModelForm):
    class Meta:
        model=Topic
        fields=[
            'title',
            'category',
            'message',
        ]
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'hoge'}),
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '選択して下さい'

    def save(self, user, commit=True, **kwargs):
        topic = super().save(commit=False)
        topic.user = user
        if commit:
            topic.save()
        return topic

class TopicForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=255, required=True,)
    user_name = forms.CharField(label='名前', max_length=30, required=True, widget=forms.TextInput(attrs={'value': '名無し'}),)
    category = forms.ModelChoiceField(label='カテゴリー', queryset=Category.objects.all(), required=True, empty_label='選択して下さい',)
    message = forms.CharField(label='本文', widget=forms.Textarea, required=True,)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)