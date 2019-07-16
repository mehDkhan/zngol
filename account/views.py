from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


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


class UserDetails(LoginRequiredMixin,DetailView):
    model = get_user_model()