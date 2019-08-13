from django.urls import path
from weather.views import home, delete_city


urlpatterns = [
    path('', home, name='home'),
    path('delete/<city>/', delete_city, name='delete_city')
]
