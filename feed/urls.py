from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('list',views.post_list,name='post_list'),
    path('new',views.new,name='new_post'),
    path('<int:pk>/<slug:slug>', views.PostDetail.as_view(), name='post_details'),
]