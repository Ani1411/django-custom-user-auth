from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserModel


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "is_staff", "is_active", "date_joined",)


admin.site.register(UserModel, CustomUserAdmin)
