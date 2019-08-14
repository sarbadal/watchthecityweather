import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from accounts.models import CustomUser
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from users.token import activation_token


# Create your views here.
def get_client_ip(request):
    """Get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def register(request, *args, **kwargs):
    """User registration view"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_active = False
            instance.save()

            site = get_current_site(request)
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            message_html = render_to_string(
                'users/verify_email.html',
                {
                    'user': instance,
                    'username': username,
                    'first_name': first_name,
                    'email': email,
                    'domain': site.domain,
                    'uid': instance.id,
                    'token': activation_token.make_token(instance)
                }
            )
            send_mail(
                'Confirmation message - watchthecityweather.com',
                message_html,
                'watchthecityweather@gmail.com',
                [email],
                fail_silently=True
            )

            return render(request, 'users/registration_start.html')
            # return redirect('login')
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
    ip = get_client_ip(request)
    # ip = request.META.get('HTTP_X_REAL_IP')
    access_key = '72705c363fc9ce983c3207a727db7f37'
    send_url = f"http://api.ipstack.com/{ip}?access_key={access_key}"
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


def activate_user_account(request, uid, token):
    """activate user account through email"""
    user = get_object_or_404(CustomUser, pk=uid)

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return render(request, 'users/registration_complete.html')

    else:
        return render(request, 'users/registration_error.html')
