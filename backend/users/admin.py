# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from users.models import User


class UserAdmin(BaseUserAdmin):

    list_display = ('email', 'is_active')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email', )
    fieldsets = (
        (None, {'fields': (
            'email', 'email_confirmed', 'password')}),
        (_('Personal info'), {'fields': (
            'first_name', 'last_name', 'location')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2'),
        }),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
    )

    change_actions = ('login_as_user', )

    def get_change_actions(self, request, object_id, form_url):
        if request.users.is_superuser:
            return super(UserAdmin, self).get_change_actions(
                request, object_id, form_url)
        return []

    def login_as_user(self, request, obj):
        from django_su.views import login_as_user
        request.method = 'POST'
        return login_as_user(request, obj.id)

    login_as_user.label = "Login as user"
    login_as_user.attrs = {
        'label_icon': "icon-user icon-alpha75",
    }


admin.site.register(User, UserAdmin)
