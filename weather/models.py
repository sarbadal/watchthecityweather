from django.db import models
from accounts.models import CustomUser

# Create your models here.


class City(models.Model):
    """Docstring"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50, verbose_name='city')

    def __str__(self):
        return self.city_name

    class Meta:
        """Docstring Meta class"""
        verbose_name_plural = 'cities'
