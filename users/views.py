import json
import requests
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request, *args, **kwargs):
    """User registration view"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')

            messages.success(
                request,
                'Your account has been created! You are now able to log in'
            )

            mail_body = """
            Hi {}!
            
            We're so happy you're here. We buuilt watchthecityweather.com to 
            provide simple possible way to watch weather. We hope that you will
            love the simplicity of this App.
            
            You can use {} or {} to sign in.
            
            
            Best,
            www.watchthecityweather.com team!
            
            """.format(first_name, username, email)

            send_mail(
                'Welcome to Weather App!',
                mail_body,
                'watchthecityweather@gmail.com',
                [email],
                fail_silently=True
            )

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(
        request,
        'users/register.html',
        {
            'form': form,
            'title': 'Registration'
        }
    )


@login_required
def profile(request):
    """Docstring"""
    ip = request.META.get('HTTP_X_REAL_IP')
    access_key = '72705c363fc9ce983c3207a727db7f37'
    send_url = f"https://api.ipstack.com/{ip}?access_key={access_key}"
    geo_req = requests.get(send_url).json()
    city = geo_req.get('city')
    country = geo_req.get('country_name')

    print(send_url)

    if country is not None:
        location = city + ', ' + country if city is not None else country
        flag = geo_req.get('country_code').lower() + ".svg"
    else:
        location = 'Could not locate'
        flag = 'None'

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'location': location,
        'country_flag': flag,
        'title': 'Profile',
    }

    return render(request, 'users/profile.html', context)


@login_required
def change_password(request):
    """Docstring"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request,
                'Your password was successfully updated!'
            )

            return redirect('home')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'users/change_password.html',
        {'form': form, 'title': 'Change Password'}
    )
