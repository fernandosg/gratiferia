from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from apps.users.models import User

# Create your views here.
class HomeView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "home/index.html", locals())


class SignupView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "home/signup.html", locals())

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        name = request.POST.get("name")
        first_last_name = request.POST.get("first_last_name")
        second_last_name = request.POST.get("second_last_name")
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if not ((password1 and password2) and password1 == password2):
            messages.error(request, "No coinciden las contraseñas")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "La contraseña ya existe")
        else:
            user = User.objects.create(email=email, name=name, first_last_name=first_last_name, second_last_name=second_last_name)
            user.set_password(password1)
            user.save()
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            next = request.session.pop('next', '/')
            return redirect(next)
        return render(request, "home/signup.html", locals())


class LoginView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "home/login.html", locals())

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        print(check_password(password, user.password))
        if not user:
            messages.error(request, 'No hay una cuenta con el email registrado')
        elif not check_password(password, user.password):
            messages.error(request, 'Contraseña incorrecta')
        else:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            next = request.session.pop('next', '/')
            return redirect(next)
        return render(request, "home/login.html", locals())


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
