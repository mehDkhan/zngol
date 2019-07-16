from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('core:index')
        else:
            form = UserCreationForm()
        return render(request, 'registration/register.html', {'form':form})
    else:
        return redirect('core:index')


def profile(request,username):
    user = User.objects.get(username=username)
    return render(request, 'account/profile.html', {'user':user})