from django.urls import path,re_path,include
from . import views

app_name = 'account'

urlpatterns= [
    path('accounts/register',views.register,name='register'),
    re_path(r'^(?P<username>\w+)$',views.UserDetails.as_view(),name='details'),
    path('', include('django.contrib.auth.urls')),

]