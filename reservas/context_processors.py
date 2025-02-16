from django.contrib.auth.models import Group

def navbar_context(request):
    """
    Determina qué navbar debe mostrarse según el tipo de usuario autenticado.
    """
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return {'navbar_template': 'layouts/base_ok.html'}
        elif request.user.groups.filter(name="Administrador Dueño").exists():
            return {'navbar_template': 'layouts/base_ok.html'}
        elif request.user.groups.filter(name="Vendedor").exists():
            return {'navbar_template': 'layouts/base_ok.html'}
        else:
            return {'navbar_template': 'layouts/base_ok.html'}   
    return {'navbar_template': 'layouts/base_log.html'}  # Si el usuario no está autenticado, no carga nada
