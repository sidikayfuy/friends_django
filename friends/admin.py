from django.contrib import admin
from django import forms

from .models import CustomUser, FriendRequest


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'friends']


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserForm
    readonly_fields = ("friends",)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
