from django.shortcuts import render, redirect
from .forms import PostCreateForm
from .models import Post
# Create your views here.

def post_list(request):
    context = {
      'post_list': Post.objects.all(),
    }
    return render(request, 'post/list.html', context)

def post_create(request):
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('snsapp:post_list')
    else:
        form = PostCreateForm()
    return render(request, 'post/create.html', {'form': form})