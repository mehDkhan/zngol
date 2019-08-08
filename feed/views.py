from django.http import JsonResponse
from django.shortcuts import render
from .models import Post,Comment
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


@require_POST
@login_required
@csrf_exempt
def post_list(request):
    post_list_ = Post.objects.all()
    page = request.POST.get('page',1)
    paginator = Paginator(post_list_,10)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request,'feed/post_list.html',{'post_list':posts})


class PostDetail(LoginRequiredMixin,DetailView):
    model = Post

