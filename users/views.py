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
    """Docstring"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')

            messages.success(request, f'Your account has been created! You are now able to log in')
            
            send_mail(
                'Welcome to Weather App!',
                'Hi {}! \nThanks for joining us. You can use {} or email to sign in.'.format(first_name, username),
                'watchthecityweather@gmail.com',
                [email],
                fail_silently=True
            )

            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Docstring"""
    send_url = "http://api.ipstack.com/check?access_key=72705c363fc9ce983c3207a727db7f37"
    geo_req = requests.get(send_url).json()
    city = geo_req['city']
    country = geo_req['country_name']

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
        'location': city + ', ' + country if city is not None else country,
        'country_flag': geo_req['country_code'].lower() + ".svg"
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
            messages.success(request, 'Your password was successfully updated!')

            return redirect('home')
            
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})
