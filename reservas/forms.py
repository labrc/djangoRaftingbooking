    
from django import forms
from .models import Balsa, Usuario, Bajada, Recorrido, BajadaBalsa
from django.contrib import messages 

# class BajadaForm(forms.ModelForm):
#     class Meta:
#         model = Bajada
#         fields = ['fecha', 'horario', 'recorrido']

#     fecha = forms.DateField(
#         widget=forms.DateInput(attrs={'class': 'datepicker', 'autocomplete': 'off'}),
#         label="Fecha de la actividad"
#     )

#     horario = forms.ChoiceField(
#         choices=Bajada.HORARIOS,
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Horario disponible"
#     )

#     recorrido = forms.ModelChoiceField(
#         queryset=Recorrido.objects.all(),
#         widget=forms.Select(attrs={'class': 'form-control'}),
#         label="Tipo de Recorrido"
#     )


class BajadaForm(forms.ModelForm):
    class Meta:
        model = Bajada
        fields = ['fecha', 'horario', 'recorrido']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.Select(attrs={'class': 'form-control'}),  # Dropdown de Horario
            'recorrido': forms.Select(attrs={'class': 'form-control'}),  # Dropdown de Recorrido
        }


class BalsaForm(forms.ModelForm):
    class Meta:
        model = Balsa
        fields = ['nombre', 'capacidad', ]

    capacidad = forms.CharField(
        max_length=3, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': '9', 'class': 'form-control'})
    )



class RecorridoForm(forms.ModelForm):
    class Meta:
        model = Recorrido
        fields = ['nombre', 'clase']  # Solo los campos definidos en el modelo Recorrido

    # Opcional: se puede añadir una etiqueta personalizada o un atributo CSS
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Nombre del Recorrido"
    )

    clase = forms.ChoiceField(
        choices=Recorrido.TIPOS,  # Utilizamos las opciones definidas en el modelo
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Tipo de Recorrido"
    )




class AddUserForm(forms.ModelForm):
    documento = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="DNI (ID Único)"
    )

    edad = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d'],
        label="Fecha de Nacimiento"
    )

    bajadas = forms.ModelMultipleChoiceField(
        queryset=Bajada.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona una o más Fechas"
    )
    def save(self, user, commit=True):
        instance = super().save(commit=False)
        if not instance.pk and not instance.created_by:  # Solo si es nuevo
            instance.created_by = user
        instance.updated_by = user  # Siempre se actualiza en modificaciones
        if commit:
            instance.save()
        return instance


    class Meta:
        model = Usuario
        fields = ['documento', 'apellido', 'nombre', 'edad', 'comentarios', 'valor_pago', 'telefono', 'email', 'bajadas']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        
        if commit:
            usuario.save()
            self.save_m2m()  # Asegurar que ManyToManyField se guarde correctamente
        
        return usuario
