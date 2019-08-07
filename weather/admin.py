from django.contrib import admin
from weather.models import City


# Register your models here.

class CityAdmin(admin.ModelAdmin):
    """class docstring"""
    list_display = ['user', 'city_name']

admin.site.register(City, CityAdmin)
