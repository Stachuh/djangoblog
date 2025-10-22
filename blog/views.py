from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from pyexpat.errors import messages

from .models import Post, RegisterForm
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .forms import PostForm, CommentForm
from django.views.generic import DetailView, TemplateView
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth import logout



class Image(TemplateView):
    form = PostForm
    template_name = 'blog/image.html'


    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('image_display', kwargs={'pk': obj.id}))

        context = self.get_context_data(form=form)
        return self.render_to_response(context)


    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

class Video(TemplateView):
    form = PostForm
    template_name = 'blog/video.html'
    def post(self,request,*args,**kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return HttpResponseRedirect(reverse_lazy('video_display', kwargs={'pk': obj.id}))
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
    def get(self,request,*args,**kwargs):
        return self.post(request,*args,**kwargs)

class VideoDisplay(TemplateView):
    model = Post
    template_name = 'blog/video_display.html'
    context_object_name = 'video'


class ImageDisplay(DetailView):
    model = Post
    template_name = 'blog/image_display.html'
    context_object_name = 'image'




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    komętarze = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/post_detail.html',{'post':post,'form':form,'komętarze':komętarze})


def error404_view(request,exception):
    data = {'name': 'Blog dla programistów'}
    return render(request,'blog/404.html',data)


def post_new(request):

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'blog/post_edit.html',{'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'blog/post_edit.html',{'form':form})




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Konto zostało utworzone!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request,'blog/register.html',{'form':form})



def logout_get(request):
    logout(request)
    return redirect('post_list')

def base(request):
    return render(request, 'base.html')


def user(request,pk):
    post = get_object_or_404(Post, pk=pk)
    posts = Post.objects.filter(author=post.author)
    return render(request, 'blog/user.html', {'post':post,'posts':posts})