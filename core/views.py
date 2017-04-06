from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserCreateForm, ArticleForm
from .models import Article


def home(request):
    return render(request, 'core/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print('was valid')
            return HttpResponse("Registration complete! Please head over to the <a href='/login/'>login page</a> to start using your website.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/login.html', {'form': form})

def json_signup(request):
    if request.method == 'POST':
        return UserCreateForm(data=request.POST).save()

def article_list(request):
    articles = Article.objects.filter(
        published_date__lte=timezone.now(),
        author=request.user).order_by('published_date')
    return render(request, 'core/article_list.html', {'articles': articles})

def article_detail(request, pk):
    # Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'core/article_detail.html', {'article': article})

def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm()
    return render(request, 'core/article_edit.html', {'form': form})

def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'core/article_edit.html', {'form': form})
