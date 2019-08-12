import os
from django.core.validators import FileExtensionValidator
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from PIL import Image


# Create your models here.
class Profile(models.Model):
    """User Profile model"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name='City')
    about_me = models.TextField(blank=True, null=True, verbose_name='About me')

    def __str__(self):
        return f'{self.user.username} Profile'


    class Meta:
        """Meta class"""
        verbose_name_plural = 'User Profile'


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    """create profile"""
    if created:
        Profile.objects.create(user=instance)
