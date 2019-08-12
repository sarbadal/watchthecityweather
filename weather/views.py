import requests
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from weather.models import City
from weather.forms import CityForm

# Create your views here.
def home(request):
    """Docstring"""
    unit = 'metric'  # 'imperial'
    appid = '822a96e083d1adb70682a06d37e42df6'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}'

    if request.method == 'POST':
        user_to_add = request.user
        city_to_add = request.POST['city_name']

        r = requests.get(url.format(city_to_add, unit, appid)).json()

        if r['cod'] == 200:

            city_country = "{}, {}".format(r['name'], r['sys']['country'])
            existing_city_count = City.objects.filter(
                Q(city_name__iexact=city_country) &
                Q(user=user_to_add)
            ).count()

            if existing_city_count == 0:

                city = "{}, {}".format(r['name'], r['sys']['country'])
                city_obj = City.objects.create(user=user_to_add, city_name=city)
                city_obj.save()

                messages.success(request, 'City has been added successfully!')

            else:
                messages.info(request, 'City is already in the list')

        else:
            messages.error(request, 'City not found')

    try:
        cities = City.objects.filter(user=request.user)
        weather_data = []

        for city in cities:
            r = requests.get(url.format(city, unit, appid)).json()

            city_weather = {
                'city': city.city_name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'iso': '{}.svg'.format(r['sys']['country'].lower()),
                'min_temp': r['main']['temp_min'],
                'max_temp': r['main']['temp_max'],
                'humidity': r['main']['humidity'],
                'wind_speed': round(r['wind']['speed'] * 3.6, 2)
            }

            weather_data.append(city_weather)

        weather_data.reverse()
        context = {
            'weather_data': weather_data,
            'form': CityForm()
        }

        return render(request, 'home/home.html', context)

    except:
        return render(request, 'home/home.html', {'form': CityForm()})


def delete_city(request, city):
    """Delete city from home page"""
    r = City.objects.filter(Q(city_name=city) & Q(user=request.user))
    r.delete()

    return redirect('home')


def temperature_toggle(request, cf):
    """temp toggle"""

    print(request.GET)
    return redirect('home')

