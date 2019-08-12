from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import CustomUser
from accounts.forms import UserCreationForm

# Register your models here.
admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    """Docstring"""
    add_form = UserCreationForm

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_admin',
        'is_staff'
    )
    list_filter = ('is_admin',)
    fieldsets = (
        (
            None, {
                'fields': (
                    'username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_active',
                    'is_staff',
                    'password'
                )
            }
        ),
        ('Permissions', {
            'fields': ('is_admin',)
        })
    )

    search_fields = ('username', 'email')
    ordering = ('username', 'email')

    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)
