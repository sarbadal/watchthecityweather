from django.contrib import admin
from users.models import Profile

# Register your models here.
admin.site.site_header = 'Weather Admin Page'


class ProfileAdmin(admin.ModelAdmin):
    """class docstring"""
    list_display = ['user', 'city']


admin.site.register(Profile, ProfileAdmin)
