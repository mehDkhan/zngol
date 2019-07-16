from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserChangeForm,CustomUserCreationForm


class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
            ('User Profile', {'fields': ('name',)}),
    ) + UserAdmin.fieldsets
    list_display = ('username','name','is_superuser')
    search_fields = ['name',]


admin.site.register(User,UserAdmin)