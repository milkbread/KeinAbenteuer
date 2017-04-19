from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import RequestContext
from django.utils import timezone


from .forms import UserCreateForm, ArticleForm, ImageForm
from .models import Article, Image


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

@login_required
def article_new(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)

    if request.method == "POST":
        form = ArticleForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Image.objects.none())
        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()

            for form in formset.cleaned_data:
                image = form['image']
                photo = Image(article=article, image=image)
                photo.save()

            messages.success(request,
                             "Yeeew,check it out on the home page!")
            return redirect('article_detail', pk=article.pk)
        else:
            print(postForm.errors, formset.errors)

    else:
        form = ArticleForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(
        request, 'core/article_edit.html', {'form': form, 'formset': formset})


@login_required
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=1)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=article.images.get_queryset())
        if form.is_valid() and formset.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_date = timezone.now()
            article.save()
            for form in formset.cleaned_data:
                if 'image' in form:
                    image = form['image']
                    photo = Image(article=article, image=image)
                    photo.save()

            return redirect('article_detail', pk=article.pk)
        else:
            print(postForm.errors, formset.errors)
    else:
        form = ArticleForm(instance=article)
        formset = ImageFormSet(queryset=article.images.get_queryset())
    return render(
        request, 'core/article_edit.html', {'form': form, 'formset': formset})
