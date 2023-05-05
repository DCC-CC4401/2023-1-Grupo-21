from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import NuevoRegistro


def register_user(request):
    if request.method == 'GET':  # si estamos cargando la página
        return render(request, "login/register_user.html")  # Mostrar el template

    elif request.method == 'POST':  # si estamos recibiendo el form de registro
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/login')
        else:
            form = UserCreationForm()
        return render(request, 'login/register_user.html', {'form': form})


def login_user(request):
    if request.method == 'GET':
        return render(request, "login/login_user.html")

    elif request.method == 'POST':
        nombre = request.POST['nombre']
        contraseña = request.POST['contraseña']
        user = authenticate(request, username=nombre, password=contraseña)

        if user is not None:
            login(request, user)
            return redirect('/movimientos')  # redirige a la página de inicio después de iniciar sesión.
        else:
            error_message = 'Usuario o contraseña incorrectos'
            return render(request, 'login/login_user.html', {'error_message': error_message})

    else:
        return render(request, 'login/login_user.html')
