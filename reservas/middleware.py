from django.shortcuts import redirect
from django.urls import reverse

class RoleBasedAccessMiddleware:
    """
    Middleware para controlar el acceso a las vistas de `reservas`:
    - `index` y `about` → Público (sin autenticación).
    - Todas las demás vistas → Requieren autenticación.
    - `config` → Solo accesible para superusuarios.
    """
    EXCLUDE_URLS = ["/", reverse("index"), reverse("about"), reverse("login"), reverse("register"), reverse("logout"),"adminpage",reverse("no_access") ]  # Páginas públicas
    ADMIN_ONLY_URLS = [reverse("config"),reverse("recorridos"),reverse("recorrido_nuevo"),"eliminar_recorrido","editar_recorrido",reverse("balsas"),"editar_balsa","eliminar_balsa",reverse("balsa")]  # Solo para administradores

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        # 1️⃣ 🔹 Si no está autenticado y la URL no es pública → Redirigir al login
        if not user.is_authenticated and path not in self.EXCLUDE_URLS:
            return redirect(reverse("login") + f"?next={path}")

        # 2️⃣ 🔹 Si la URL es de admins (`config`) y no es superusuario → Redirigir a inicio
        if path in self.ADMIN_ONLY_URLS and not user.is_superuser:
            return redirect(reverse("no_access"))

        return self.get_response(request)
