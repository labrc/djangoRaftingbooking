from django.db import models
import re

from django.contrib.auth.models import User


class Recorrido(models.Model):
    
    TIPOS = [
        ('normal', 'Rafting normal'),
        ('frontera', 'Rafting de frontera'),
    ]
    
    nombre = nombre = models.CharField(max_length=50)
    clase = models.CharField(max_length=50, choices=TIPOS, unique=False)
    def __str__(self):
        return f"{self.nombre} - {self.clase} "

class Bajada(models.Model):
    HORARIOS = [
        ('08:00', 'Mañana'),
        ('12:00', 'Tarde'),
        ('16:00', 'Extra'),
    ]
    
    fecha = models.DateField()
    horario = models.CharField(max_length=5, choices=HORARIOS)
    recorrido = models.ForeignKey(Recorrido, on_delete=models.CASCADE, related_name='bajadas')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Agregar automáticamente todas las balsas a la bajada
        for balsa in Balsa.objects.all():
            BajadaBalsa.objects.get_or_create(bajada=self, balsa=balsa)
    
    def __str__(self):
        return f" Bajada {self.recorrido} - {self.fecha} {self.horario}"

class Balsa(models.Model):
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.nombre} ({self.capacidad} personas)"

class BajadaBalsa(models.Model):
    bajada = models.ForeignKey(Bajada, on_delete=models.CASCADE, related_name='bajada_balsas')
    balsa = models.ForeignKey(Balsa, on_delete=models.CASCADE, related_name='bajada_balsas')

    def __str__(self):
        return f"{self.balsa.nombre} en {self.bajada}"




class Usuario(models.Model):
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    edad = models.DateField()
    documento = models.CharField(max_length=50, primary_key=True)  # DNI como clave primaria
    comentarios = models.TextField(blank=True, null=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bajadas = models.ManyToManyField("Bajada", related_name="navegantes")

    # Nuevo: información sobre quién lo creó/modificó y cuándo
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="usuarios_creados")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="usuarios_modificados")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # Recibir usuario desde la vista
        skip_validation = kwargs.pop("skip_validation", False)

        if user:
            if not self.pk and not self.created_by:  # Si el usuario es nuevo y no tiene creador
                self.created_by = user  # Se asigna solo en la creación
            self.updated_by = user  # Siempre se actualiza en modificaciones

        if not skip_validation:
            # Formateamos el número de teléfono
            if self.telefono:
                self.telefono = self.format_phone_number(self.telefono)

            # Validación de la capacidad de la bajada
            if self.bajadas.exists():
                for bajada in self.bajadas.all():
                    self._check_capacity_for_bajada(bajada)

        super().save(*args, **kwargs)


    def _check_capacity_for_bajada(self, bajada):
        if not bajada:  
            return  # ✅ No validar si no hay bajada seleccionada

        capacidad_total = sum(balsa.capacidad for balsa in Balsa.objects.all() if balsa.capacidad)

        if capacidad_total == 0:
            raise ValueError(f"La bajada del {bajada.fecha} no tiene balsas asignadas con capacidad disponible.")

        # ✅ Solo validar si se está agregando una nueva bajada
        if self.pk and self.bajadas.filter(pk=bajada.pk).exists():
            return  # ✅ Si el usuario ya estaba en esta bajada, no validar

        if bajada.navegantes.count() >= capacidad_total:
            raise ValueError(f"No se pueden agregar más navegantes en la bajada del {bajada.fecha}. Capacidad máxima ({capacidad_total}) alcanzada.")



    def format_phone_number(self, phone_number):
        phone_number = re.sub(r'[^\d+]', '', phone_number)
        if phone_number.startswith('+'):
            phone_number = '+' + ''.join(re.findall(r'\d', phone_number[1:]))
        else:
            phone_number = ''.join(re.findall(r'\d', phone_number))
        return phone_number

    def __str__(self):
        return (self.apellido + ", " + self.nombre)


