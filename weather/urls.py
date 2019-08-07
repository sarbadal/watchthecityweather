from django.urls import path
from weather.views import home, delete_city, temperature_toggle

urlpatterns = [
    path('', home, name='home'),
    # path('cf/<cc>/', temperature_toggle, name='temp_toggle'),
    path('delete/<city>/', delete_city, name='delete_city')
]