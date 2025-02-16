from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum, Count,OuterRef,Subquery
from .forms import AddUserForm, BalsaForm, BajadaForm, RecorridoForm
from .models import Balsa, Usuario, Bajada, Recorrido
import csv
from io import StringIO

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Bajada

from django.utils.timezone import now 


def index(request):
    return render(request, 'index.html')

def acceso(request):
    return render(request, 'no_access.html')

def config(request):
    return render(request, 'config.html')




from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from openpyxl import load_workbook
import os

def exportar_planilla(request, bajada_id):
    # Obtener la bajada y sus navegantes
    bajada = get_object_or_404(Bajada, id=bajada_id)
    navegantes = bajada.navegantes.all()

    # Ruta de la planilla base (asegúrate de que exista en el proyecto)
    template_path = os.path.join("reservas/static/assets/planilla_base.xlsx")

    
    # Cargar la planilla original
    wb_original = load_workbook(template_path)
    ws_original = wb_original.active

    # Insertar la fecha en C9 y C10
    fecha_bajada = bajada.fecha.strftime("%d/%m/%Y")
    ws_original["C9"] = fecha_bajada
    ws_original["C10"] = fecha_bajada

    # Insertar los navegantes en la tabla (desde C13 en adelante)
    start_row = 13
    for i, nav in enumerate(navegantes):
        row = start_row + i
        ws_original[f"C{row}"] = nav.documento
        ws_original[f"D{row}"] = nav.apellido
        ws_original[f"E{row}"] = nav.nombre
        ws_original[f"F{row}"] = nav.edad.strftime("%d/%m/%Y") if nav.edad else ""

    # Crear respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="Planilla_Bajada_{bajada.fecha}.xlsx"'

    # Guardar en la respuesta
    wb_original.save(response)
    return response





def bajadas(request):
    bajadas = Bajada.objects.prefetch_related('navegantes').all()  
    
    return render(request, 'bajadas.html', {'bajadas': bajadas})

def obtener_bajadas_json(request):
    bajadas = Bajada.objects.values('fecha', 'horario')
    eventos = [{'title': b['horario'], 'start': b['fecha']} for b in bajadas]
    return JsonResponse(eventos, safe=False)

def nueva_bajada(request):
    bajadasLlenas = (
        Bajada.objects.values("fecha")
        .annotate(total=Count("horario"))
        .filter(total=3)
        .values_list("fecha", flat=True)
    )
    fechas_ocupadas = list(bajadasLlenas)

    if request.method == "POST":
        form = BajadaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bajadas')
        else:
            print("❌ Errores del formulario:", form.errors)  # 🔴 Depuración en logs

    else:
        form = BajadaForm()

    return render(request, "bajadas_nueva.html", {"form": form, "fechas_ocupadas": fechas_ocupadas})

from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

@user_passes_test(lambda u: u.is_superuser)
def borrar_bajada(request, bajada_id):
    bajada = get_object_or_404(Bajada, id=bajada_id)
    bajada.delete()
    return HttpResponseRedirect(reverse('bajadas'))


def obtener_bajadas_json(request):
    bajadas = Bajada.objects.values('fecha', 'horario')
    return JsonResponse(list(bajadas), safe=False)



def editar_bajada(request, bajada_id):
    bajada = get_object_or_404(Bajada, id=bajada_id)

    if request.method == 'POST':
        form = BajadaForm(request.POST, instance=bajada)
        if form.is_valid():
            form.save()
            messages.success(request, "Bajada actualizada correctamente.")
            return redirect('bajadas')  # Redirige a la lista de bajadas
    else:
        form = BajadaForm(instance=bajada)

    return render(request, 'editar_bajada.html', {'form': form, 'bajada': bajada})


from django.core.paginator import Paginator
from django.utils import timezone



def lista_bajadas(request):
    # Determinar si se están viendo las bajadas pasadas
    modo_pasado = request.GET.get('modo', 'futuras') == 'pasadas'

    if modo_pasado:
        bajadas = Bajada.objects.filter(fecha__lt=timezone.now()).order_by('-fecha')
    else:
        bajadas = Bajada.objects.filter(fecha__gte=timezone.now()).order_by('fecha')

    # Aplicar paginación (4 por página)
    paginator = Paginator(bajadas, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'bajadas.html', {
        'page_obj': page_obj,
        'modo_pasado': modo_pasado
    })


def balsas(request):
    balsas = Balsa.objects.all()
    return render(request, 'balsas.html', {'balsas': balsas})

def nueva_balsa(request):
    if request.method == "POST":
        form = BalsaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('balsas')
    else:
        form = BalsaForm()
    return render(request, "BalsaNueva.html", {"form": form})

def editar_balsa(request, balsa_id):
    balsa = get_object_or_404(Balsa, id=balsa_id)
    if request.method == 'POST':
        form = BalsaForm(request.POST, instance=balsa)
        if form.is_valid():
            form.save()
            return redirect('balsas')
    else:
        form = BalsaForm(instance=balsa)
    return render(request, 'editar_balsa.html', {'form': form, 'balsa': balsa})

def eliminar_balsa(request, balsa_id):
    balsa = get_object_or_404(Balsa, id=balsa_id)
    if request.method == 'POST':
        balsa.delete()
        return redirect('balsas')
    return render(request, 'balsa_confirm_delete.html', {'balsa': balsa})

from django.core.paginator import Paginator

def navegantes(request):
    # Obtener la fecha de la bajada más próxima para cada usuario
    subquery_proxima_bajada = (
        Bajada.objects.filter(navegantes=OuterRef("documento"), fecha__gte=now())
        .order_by("fecha")
        .values("id")[:1]
    )

    # Anotar la fecha de la bajada más próxima para cada navegante
    usuarios = Usuario.objects.annotate(
        proxima_bajada_id=Subquery(subquery_proxima_bajada)
    ).order_by("proxima_bajada_id", "-created_at")

    # Agrupar usuarios por su bajada
    usuarios_agrupados = {}
    for usuario in usuarios:
        primera_bajada = usuario.bajadas.first() if usuario.bajadas.exists() else None
        usuario.primera_bajada = primera_bajada

        if primera_bajada:
            if primera_bajada.id not in usuarios_agrupados:
                usuarios_agrupados[primera_bajada.id] = {
                    "bajada": primera_bajada,
                    "navegantes": [],
                }
            usuarios_agrupados[primera_bajada.id]["navegantes"].append(usuario)
        else:
            if "sin_bajada" not in usuarios_agrupados:
                usuarios_agrupados["sin_bajada"] = {
                    "bajada": None,
                    "navegantes": [],
                }
            usuarios_agrupados["sin_bajada"]["navegantes"].append(usuario)

    # Convertimos a lista para la paginación
    usuarios_list = list(usuarios_agrupados.values())

    # Paginación con 10 elementos por página
    paginator = Paginator(usuarios_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "navegantes.html", {"page_obj": page_obj}) 

def eliminar_navegante(request, documento):
    user = get_object_or_404(Usuario, documento=documento)
    if request.method == 'POST':
        user.delete()
        return redirect('navegantes')
    return render(request, 'user_confirm_delete.html', {'usuario': user})

def nuevo_navegante(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            documento = form.cleaned_data['documento']

            # Verificar si el usuario ya existe
            usuario, creado = Usuario.objects.get_or_create(
                documento=documento,
                defaults={
                    'apellido': form.cleaned_data['apellido'],
                    'nombre': form.cleaned_data['nombre'],
                    'edad': form.cleaned_data['edad'],
                    'email': form.cleaned_data['email'],
                    'telefono': form.cleaned_data['telefono'],
                    'valor_pago': form.cleaned_data['valor_pago'],
                    'comentarios': form.cleaned_data['comentarios'],
                    'created_by': request.user,  # ✅ Asignar creador
                    'updated_by': request.user  # ✅ También inicializar updated_by
                }
            )

            if not creado:
                messages.warning(request, "Este navegante ya existe.")
            else:
                messages.success(request, "Usuario agregado exitosamente.")

            # ✅ Corrección: Usar .set() para ManyToManyField
            usuario.bajadas.set(form.cleaned_data['bajadas'])

            usuario.updated_by = request.user  # ✅ Asegurar que updated_by siempre se registre
            usuario.save()  # Guardar el objeto con la actualización

            return redirect('navegantes')

    else:
        form = AddUserForm()

    return render(request, 'addnav.html', {'form': form})


def editar_navegante(request, documento):
    usuario = get_object_or_404(Usuario, documento=documento)

    if request.method == 'POST':
        form = AddUserForm(request.POST, instance=usuario)
        
        if form.is_valid():
            usuario = form.save(commit=False)  # Guardar pero sin confirmar aún
            usuario.updated_by = request.user  # ✅ Registrar el usuario que lo modificó

            try:
                usuario.save()  # Intenta guardar y validar la capacidad de la bajada
                messages.success(request, "Usuario actualizado correctamente.")
                form.save_m2m()
                return redirect(request.META.get('HTTP_REFERER', 'navegantes'))
                
            except ValueError as e:
                messages.error(request, str(e))  # ✅ Capturar el error y mostrarlo en el modal

        else:
            messages.error(request, "Error al guardar los cambios. Revisa los datos ingresados.")
    
    else:
        form = AddUserForm(instance=usuario)

    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})



def obtener_bajadas_json(request):
    bajadas = Bajada.objects.values('fecha', 'horario')
    eventos = [{'title': b['horario'], 'start': b['fecha']} for b in bajadas]
    return JsonResponse(eventos, safe=False)


from io import StringIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from datetime import datetime


import re


# @csrf_exempt
# @login_required  
# def procesar_csv(request):
#     if request.method == "POST":
#         csv_text = request.POST.get("csv_data", "").strip()
#         if not csv_text:
#             return JsonResponse({"success": False, "message": "⚠️ El archivo CSV está vacío."})

#         csv_file = StringIO(csv_text)
#         reader = csv.reader(csv_file,delimiter=',')
#         #next(reader, None)  # Omitir encabezado si existe

#         errores = []
#         navegantes_agregados = 0
#         print("📌 Datos recibidos del formulario:")
#         print(csv_text)  # 🔍 Ver qué datos llegan desde el textarea

#         for row in reader:
#             print(row)  # 🔍 Imprimir cada fila del CSV
#             try:
#                 # Asegurar que hay suficientes columnas en la fila
#                 if len(row) < 4:
#                     errores.append(f"Fila incompleta: {row}")
#                     continue  # Saltar fila

#                 # Extraer datos con valores por defecto si están vacíos
#                 documento = row[0].strip()
#                 apellido = row[1].strip()
#                 nombre = row[2].strip()
#                 print(nombre) 
#                 edad = row[3].strip()
#                 print(edad) 
#                 telefono = row[4].strip() if len(row) > 4 and row[4].strip() else None
#                 email = row[5].strip() if len(row) > 5 and row[5].strip() else None
                
#                 try:
#                     # Si la fecha tiene formato dd/mm/yyyy → Convertir a yyyy-mm-dd
#                     if edad and "/" in edad:
#                         fecha_obj = datetime.strptime(edad, "%d/%m/%Y")  # Convertir a objeto fecha
#                         edad = fecha_obj.strftime("%Y-%m-%d")  # Guardar en formato correcto

#                     # Si la fecha tiene formato dd-mm-yyyy → Convertir a yyyy-mm-dd
#                     elif edad and "-" in edad:
#                         fecha_obj = datetime.strptime(edad, "%d-%m-%Y")  # Convertir a objeto fecha
#                         edad = fecha_obj.strftime("%Y-%m-%d")  # Guardar en formato correcto

#                     # Si la fecha ya está en yyyy-mm-dd, dejarla igual
#                     elif edad:
#                         edad = edad.strip()
#                 except ValueError:
#                     print(f"⚠️ Error en formato de fecha: {edad}")
#                     edad = None  # Si el formato es inválido, no lo guardamos


#                 # Validar los campos obligatorios
#                 if not documento or not apellido or not nombre or not edad:
#                     errores.append(f"Faltan datos obligatorios en fila {row}")
#                     continue

#                 # Crear el usuario
#                 navegante = Usuario(
#                     documento=documento,
#                     apellido=apellido,
#                     nombre=nombre,
#                     edad=edad,
#                     telefono=telefono,
#                     email=email,
#                     created_by=request.user,  # ✅ Guarda el usuario actual, no una fecha
#                     updated_by=request.user  # ✅ Guarda quién lo modifica                    
#                 )
#                 print(f"📝 Creando navegante: {navegante}")
#                 navegante.save()
#                 navegantes_agregados += 1

#             except IntegrityError as e:
#                 errores.append(f"Error de integridad en fila {row}: {str(e)}")
#             except Exception as e:
#                 errores.append(f"Error en fila {row}: {str(e)}")

#         # Si hubo errores, devolverlos
#         if errores:
#             return JsonResponse({
#                 "success": False,
#                 "message": "⚠️ Algunos registros tuvieron errores.",
#                 "errors": errores
#             })
        
#         # Si no hubo errores, devolver éxito
#         return JsonResponse({
#             "success": True,
#             "message": f"✅ {navegantes_agregados} navegantes agregados correctamente."
#         })

#     return JsonResponse({"success": False, "message": "❌ Método inválido."})

import csv
import re
from io import StringIO
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Usuario
from datetime import datetime, date


def detectar_formato(lineas):
    """Detecta si la entrada es CSV o texto separado por líneas"""
    if "," in lineas[0]:  
        return "csv"
    return "multi-line"


@login_required
@csrf_exempt
def procesar_csv(request):
    if request.method == "POST":
        csv_text = request.POST.get("csv_data", "").strip()
        bajada_id = request.POST.get("bajada_id")  # ✅ Obtener la bajada seleccionada

        if not csv_text:
            return JsonResponse({"success": False, "message": "⚠️ El archivo CSV está vacío."})

        lineas = [line.strip() for line in csv_text.split("\n") if line.strip()]
        errores = []
        navegantes_agregados = 0
        usuarios = []

        formato = detectar_formato(lineas)
        print(f"📌 Formato detectado: {formato}")

        if formato == "csv":
            for i, line in enumerate(lineas):
                try:
                    columnas = line.split(",")
                    if len(columnas) < 4:
                        errores.append(f"⚠️ Faltan datos en la fila {i+1}: {line}")
                        continue

                    dni = columnas[0].strip()
                    apellido = columnas[1].strip()
                    nombre = columnas[2].strip()
                    fecha_nacimiento = columnas[3].strip()
                    edad = formatear_fecha(fecha_nacimiento)

                    if edad is None:
                        errores.append(f"⚠️ Fecha inválida en la fila {i+1}: {fecha_nacimiento}")
                        continue

                    usuarios.append((dni, apellido, nombre, edad))

                except Exception as e:
                    errores.append(f"❌ Error en fila {i+1}: {str(e)}")

        for dni, apellido, nombre, edad in usuarios:
            try:
                print(f"👤 Procesando usuario: DNI={dni}, Nombre={nombre}, Apellido={apellido}, Edad={edad}")

                navegante, created = Usuario.objects.get_or_create(
                    documento=dni,
                    defaults={
                        "apellido": apellido,
                        "nombre": nombre,
                        "edad": edad,
                        "created_by": request.user if request.user.is_authenticated else None,
                        "updated_by": request.user if request.user.is_authenticated else None,
                    },
                )

                if created:
                    navegantes_agregados += 1
                    print(f"✅ Usuario agregado: {nombre} {apellido} (DNI {dni})")

                if bajada_id:
                    bajada = get_object_or_404(Bajada, id=bajada_id)
                    navegante.bajadas.add(bajada)
                    print(f"✅ Asignada bajada {bajada_id} a {navegante.documento}")

            except Exception as e:
                errores.append(f"❌ No se pudo guardar {nombre} {apellido} (DNI {dni}): {str(e)}")
                print(f"❌ Error al guardar usuario {nombre} {apellido} (DNI {dni}): {str(e)}")
                continue  # 🔥 IMPORTANTE: Continúa con el siguiente usuario

        if errores:
            return JsonResponse({
                "success": False,
                "message": f"⚠️ {navegantes_agregados} navegantes agregados correctamente. Algunos registros fallaron.",
                "errors": errores
            })

        return JsonResponse({
            "success": True,
            "message": f"✅ {navegantes_agregados} navegantes agregados correctamente."
        })

    return JsonResponse({"success": False, "message": "❌ Método inválido."})



from datetime import datetime

def formatear_fecha(fecha):
    if not fecha or fecha.strip() == "":
        return None  # Si la fecha está vacía, retornar None

    fecha = fecha.strip()  # Eliminar espacios en blanco
    formatos = ["%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y"]  # Formatos posibles

    for fmt in formatos:
        try:
            fecha_obj = datetime.strptime(fecha, fmt)  # Intentar convertir la fecha
            return fecha_obj.strftime("%Y-%m-%d")  # Convertir a formato compatible con Django
        except ValueError:
            continue  # Si falla, intenta con el siguiente formato

    print(f"⚠️ Error: Formato de fecha inválido -> '{fecha}'")  # 🔴 Depurar si falla
    return None  # Si no coincide con ningún formato, devolver None


def agregar_por_csv(request):
    bajadas_disponibles = Bajada.objects.filter(fecha__gte=now()).order_by("fecha")  # ✅ Solo futuras bajadas
    return render(request, "agregar_csv.html", {"bajadas": bajadas_disponibles})  # 🔥 Enviar bajadas a la plantilla


def recorridos(request):
    recorridos = Recorrido.objects.all()
    return render(request, 'recorridos.html', {'recorridos': recorridos})

def nuevo_recorrido(request):
    if request.method == "POST":
        form = RecorridoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recorridos')
        form = RecorridoForm()
    return render(request, "recorrido_nuevo.html", {"form": form})

def editar_recorrido(request, recorrido_id):
    recorrido = get_object_or_404(Recorrido, id=recorrido_id)
    if request.method == 'POST':
        form = RecorridoForm(request.POST, instance=recorrido)
        if form.is_valid():
            form.save()
            return redirect('recorridos')
    else:
        form = RecorridoForm(instance=recorrido)
    return render(request, 'recorrido_nuevo.html', {'form': form, 'recorrido': recorrido})

def eliminar_recorrido(request, pk):
    recorrido = get_object_or_404(Recorrido, pk=pk)
    recorrido.delete()
    return redirect('recorridos') 

def about(request):
    return render(request, 'about.html')




from django.shortcuts import render

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)

def error_503(request, exception=None):
    return render(request, 'errors/503.html', status=503)
