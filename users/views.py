from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm

# Función para restringir solo a Superadmin
def is_superadmin(user):
    return user.is_superuser

def superadmin_required(view_func):
    return login_required(user_passes_test(is_superadmin)(view_func))

# Vista de Registro

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Usuario creado correctamente.")
            print("✅ Usuario creado correctamente.")
            return redirect("profile")
        else:
 # Obtener errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"❌ {field.capitalize()}: {error}")  # Mostrar cada error

    form = RegisterForm()  # ← Asegurar que se muestra el formulario en GET

    return render(request, "auth/profile.html", {"form": form})

# Vista de Perfil (Solo Superadmin)
@login_required
def profile(request):
    return render(request, "profile.html")


from django.contrib.auth.views import LoginView

def logout_user(request):  # Renombrado para evitar conflicto
    logout(request)
    # messages.success(request, "Sesión cerrada correctamente.")
    return redirect("index")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect("profile")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, "auth/login.html")

class CustomLoginView(LoginView):
    template_name = "auth/login.html"

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrectos.")  # Agregar mensaje de error
        print("⛔ Fallo el login!")
        return self.render_to_response(self.get_context_data(form=form))


def form_invalid(self, form):
        messages.error(self.request, "⚠️ Usuario o contraseña incorrectos.")
        print("⛔ Fallo el login!")
        return self.render_to_response(self.get_context_data(form=form))



