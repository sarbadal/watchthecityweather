from django.urls import path, include
from django.contrib.auth import views as auth_views
from users.views import change_password, profile, register
from accounts.views import login_view, logout_view

urlpatterns = [
    path('', include('weather.urls')),
    path('password-change/', change_password, name='change_password'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
]