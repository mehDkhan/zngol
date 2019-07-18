from django.shortcuts import render,redirect
from django.views.generic import DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from .forms import CustomUserCreationForm
from django.urls import reverse


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('core:index')
        else:
            form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form':form})
    else:
        return redirect('core:index')


class UserDetails(LoginRequiredMixin,DetailView):
    model = User
    slug_field = 'username'
    slug_url_kwarg = 'username'


class UserUpdate(LoginRequiredMixin, UpdateView):
    fields = ['name', 'email', 'picture','location', 'bio', ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse('account:details',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)
