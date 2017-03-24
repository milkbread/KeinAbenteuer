from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'core/home.html')


def signup(request):
    if request.method == 'POST':
        print("joooo")
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
