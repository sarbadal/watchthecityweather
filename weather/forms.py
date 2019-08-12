from django.forms import ModelForm, TextInput
from weather.models import City


class CityForm(ModelForm):
    """Docstring"""
    class Meta:
        """Meta class Docstring"""
        model = City
        fields = ['user', 'city_name']
        widgets = {
            'city_name': TextInput(
                attrs={'class': 'input', 'placeholder': 'City Name'}
            )
        }
