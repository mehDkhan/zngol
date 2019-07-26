from django.shortcuts import render,redirect
from django.views.generic import DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User,Contact
from .forms import CustomUserCreationForm
from django.urls import reverse
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse,JsonResponse

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
    model = User
    fields = ['name', 'email', 'picture','location', 'bio', ]
    template_name = 'account/update_user.html'

    def get_success_url(self):
        """send the user back to their own page after a successful update"""
        return reverse('account:details',
                       kwargs={'username': self.request.user.username})

    def get_object(self):
        """Only get the User record for the user making the request"""
        return User.objects.get(username=self.request.user.username)


@ajax_required
@require_POST
@login_required
def follow(request):
    """
    View for follow a user
    request.user wants to follow user with user_id=id
    """
    user_id = request.POST.get('user_id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if request.user == user:
                return JsonResponse({'status':0,'msg':'You can\'t follow yourself'})
            if action == 'follow':
                if request.user.is_following(user):
                    return JsonResponse({'status':0,'msg':'already following'})
                else:
                    request.user.follow(user)
                    return JsonResponse({'status':1,'msg':'followed'})
            else:
                if request.user.is_following(user):
                    request.user.unfollow(user)
                    return JsonResponse({'status':1,'msg':'un-followed'})
                else:
                    return JsonResponse({'status':0,'msg':'not following'})
        except User.DoesNotExist:
            return JsonResponse({'status':0,'msg':'user not found'})
    return JsonResponse({'status':0})