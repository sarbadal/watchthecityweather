from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class CustomUserManager(BaseUserManager):
    """Custom User Manager"""

    def create_user(self, username, email, password=None):
        """Override create_user method"""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, first_name, password=None):
        """Override superuser method"""
        user = self.create_user(username, email, password=password)
        user.first_name = first_name
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    """Custom User"""
    username = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=USERNAME_REGEX,
                message='Username must be alphanumeric or contain numbers',
                code='invalid_username'
            )
        ],
        unique=True
    )
    email = models.EmailField(max_length=510, unique=True, verbose_name='email address')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name']


    def __str__(self):
        return self.email

    def get_short_name(self):
        """The user is identified by their email address"""
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
