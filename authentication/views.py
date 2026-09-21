import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import UserRegisterForm
from users.models import Profile


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user,
                date_of_birth=form.cleaned_data.get('date_of_birth'),
                gender=form.cleaned_data.get('gender'),
                has_taken_jlpt=form.cleaned_data.get('has_taken_jlpt'),
                has_certificate=form.cleaned_data.get('has_certificate'),
                jlpt_level=form.cleaned_data.get('jlpt_level')
            )
            messages.success(request, f"Conta criada para {user.username}!")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "authentication/register.html", {'form': form})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password) if username else None

        if user is not None:
            code = str(random.randint(100000, 999999))
            request.session['2fa_user_id'] = user.id
            request.session['2fa_code'] = code

            send_mail(
                'Seu código de verificação - NihonKai',
                f'Seu código de verificação é: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            return redirect('verify_2fa')
        else:
            messages.error(request, 'Email e/ou senha incorretos.')
            return redirect('login')

    return render(request, 'authentication/login.html')


def verify_2fa(request):
    if request.method == "POST":
        code_input = request.POST.get('code')
        code_real = request.session.get('2fa_code')
        user_id = request.session.get('2fa_user_id')

        if code_input == code_real and user_id:
            user = User.objects.get(id=user_id)
            login(request, user)
            del request.session['2fa_code']
            del request.session['2fa_user_id']
            return redirect('profile')
        else:
            messages.error(request, 'Código inválido. Tente novamente.')
            return redirect('verify_2fa')

    return render(request, 'authentication/verify_2fa.html')


def logout_view(request):
    logout(request)
    return redirect('login')