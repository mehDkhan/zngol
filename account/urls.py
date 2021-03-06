from django.urls import path,re_path,include
from . import views

app_name = 'account'

urlpatterns= [
    path('register',views.register,name='register'),
    path('follow', views.follow, name='follow'),
    re_path(r'^(?P<username>\w+)$',views.UserDetails.as_view(),name='details'),
    path('', include('django.contrib.auth.urls')),
    re_path(r'^(?P<username>\w+)/update$',views.UserUpdate.as_view(),name='update'),

]