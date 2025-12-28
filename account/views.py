from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from account.form import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import CustomUser
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import Http404
import requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .form import *

from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
import secrets
import string
from random import choice
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash


# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid")
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            print("user save secsesfull")
            # Send an email with activation code
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            activation_url = f"http://{get_current_site(request).domain}/{reverse('account:activate', kwargs={'uidb64': uid, 'token': token})} "
            print("active url made secsesfull")
            send_mail(
                'Activate Your Account',
                f'Click this link to activate your account: {activation_url}',
                'mahdisharifih@gmail.com',
                [user.email],
            )
            print("send maile secsesfull")
            return redirect('account:login')
        else:
            er=form.errors
            return render(request, 'account/register.html', {'form': form, 'errors': er})
    else:
        print("sing up not secses full")

        form = UserRegisterForm()
        return render(request, 'account/register.html', {'form': form})


# Login View


def login_view(request):
    if request.method == 'POST':
        i = 1
        i += 1

        form = user_login_form(data=request.POST)
        if form.is_valid():

            # Get username and password from the form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']




            # Authenticate the user using Django's authenticate function
            user = authenticate(request, username=username, password=password)
            print(f"user={user}")

            if user is not None:
                print("user not none ")

                if user.is_active:  # Check if the user is active

                    login(request, user)  # Log the user in
                    return render(request, 'users-dashboard/dist/index.html', {'user': user})
                else:
                    print("user not active ")

                    er = 'error user not activate'
                    return render(request, 'account/login.html', {'er': er, 'form': form})
            else:
                eroore = 'errore username or password notfound'
                form = user_login_form()
            return render(request, 'account/login.html', {'form': form, 'ere': eroore})
        elif i > 1:
            # Check for specific CAPTCHA errors
            if form.errors.get('captcha'):
                eroore = 'capcha not found'
                form = user_login_form()
                return render(request, 'account/login.html', {'form': form, 'ere': eroore})

    else:
        form = user_login_form()
    return render(request, 'account/login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('account:login')  # Redirect to login after logging out


# Activate View (Email confirmation)
def activate(request, uidb64, token):
    try:
        # Decode the uid from the URL and print it for debugging
        uid = urlsafe_base64_decode(uidb64)
        user = CustomUser.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully!')
            return redirect('account:login')
        else:
            messages.error(request, 'Activation link is invalid or expired.')
            return render(request, 'account/activation_failed.html')
    except Exception as e:
        print(e)
        messages.error(request, 'Activation link is invalid or expired.')
        return render(request, 'account/activation_failed.html')


@login_required
def user_panel(request):
    user = request.user
    context = {
        'user': request.user,
        'profile': request.user.profile,  # Assuming you have a Profile model

    }
    return render(request, 'users-dashboard/src/index.html', context)


class hom_viwe(TemplateView):
    template_name = 'account/home_login.html'


def show_sit(request):
    web = ['https://goldprice.org/live-gold-price.html', 'https://www.tgju.org/']

    def try_sit(sit):
        try:
            respons = requests.get(sit)
            if respons.status_code == 404:
                return render(request, "account/base/show_sit_error.html", {"error": "404", "iframe_url": sit})
            elif respons.status_code == 403:
                return render(request, "account/base/show_sit_error.html", {"error": "403", "iframe_url": sit})
            elif respons.status_code != 200:
                return render(request, "account/base/show_sit_error.html", {"error": "other", "iframe_url": sit})

            # If the page exists, render the iframe page
            return render(request, "users-dashboard/child/show_price.html", {"iframe_url": sit})

        except requests.exceptions.RequestException:
            # If there is an error while trying to fetch the page (e.g., connection error)
            return render(request, "account/base/show_sit_error.html", {"error": "connection", "iframe_url": sit})

    try:
        response = requests.get(web[0])

        if response.status_code == 404:
            return try_sit(web[1])

        elif response.status_code == 403:
            return try_sit(web[1])
        elif response.status_code != 200:
            return try_sit(web[1])

        return render(request, "account/base/show_sit.html", {"iframe_url": web[0]})
    except requests.exceptions.RequestException:
        return try_sit(web[1])


def show_news(request):
    web = ['https://www.shahrekhabar.com/', 'https://edition.cnn.com/']

    def try_sit(sit):
        try:
            respons = requests.get(sit)
            if respons.status_code == 404:
                return render(request, "account/base/show_sit_error.html", {"error": "404", "iframe_url": sit})
            elif respons.status_code == 403:
                return render(request, "account/base/show_sit_error.html", {"error": "403", "iframe_url": sit})
            elif respons.status_code != 200:
                return render(request, "account/base/show_sit_error.html", {"error": "other", "iframe_url": sit})

            # If the page exists, render the iframe page
            return render(request, "users-dashboard/child/show_sit.html", {"iframe_url": sit})

        except requests.exceptions.RequestException:
            # If there is an error while trying to fetch the page (e.g., connection error)
            return render(request, "account/base/show_sit_error.html", {"error": "connection", "iframe_url": sit})

    try:
        response = requests.get(web[0])

        if response.status_code == 404:
            return try_sit(web[1])

        elif response.status_code == 403:
            return try_sit(web[1])
        elif response.status_code != 200:
            return try_sit(web[1])

        return render(request, "users-dashboard/child/show_sit.html", {"iframe_url": web[0]})
    except requests.exceptions.RequestException:
        return try_sit(web[1])


def forget_password(request):
    if request.method == "POST":
        form = ForgetPassword(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            Email = form.cleaned_data['Email']
            geter = CustomUser.objects.get(username=username)

            if geter.email == Email:
                def make_random_password(length=10,
                                         allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
                    return ''.join([choice(allowed_chars) for i in range(length)])

                new_password = make_random_password()
                geter.set_password(new_password)
                geter.save()
                msg = f"your new password : {new_password}"
                send_mail('recovery password', msg, 'mahdisharifih@gmail.com', [Email])
                return redirect('account:login')

    else:
        form = ForgetPassword()
    return render(request, 'account/forget_password.html', {'form': form})


class About(TemplateView):
    template_name = 'web/income/About.html'

class Home(TemplateView):
    template_name = 'account/hom_heder.html'

def edit_user_info(request):
    if request.user.is_authenticated:
        post = CustomUser.objects.get(pk=request.user.pk)
        if request.method == 'POST':
            form = Edit_info(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('web:user_info')
        else:
            form = Edit_info()

        return render(request, 'users-dashboard/child/edit_user.html', {'post': post, 'form': form})
    else:
        return redirect('account:login')


def password_change(request, pk):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=pk)

        if request.method == "POST":
            form = PasswordChangeForm(request.POST)

            if form.is_valid():
                # Check if the old password matches
                if not user.check_password(form.cleaned_data['old_password']):
                    form.add_error('old_password', 'Old password is incorrect.')
                else:
                    # If new passwords match, update the password
                    new_password = form.cleaned_data['new_password_1']
                    user.set_password(new_password)
                    user.save()

                    # Update the session with the new password
                    update_session_auth_hash(request, user)  # This keeps the user logged in

                    return redirect('web:user_info')  # Redirect to a page after success
        else:
            form = PasswordChangeForm()

        return render(request, 'users-dashboard/child/change_password.html', {'form': form})

    else:
        return redirect('account:login')



