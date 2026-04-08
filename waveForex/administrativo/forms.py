# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Usuario, Pago, SuscripcionPlataforma, Producto

class UsuarioForm(forms.ModelForm):
    contrasenia = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))

    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'contrasenia', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contrasenia = self.cleaned_data['contrasenia']  # No hashes password here
        if commit:
            usuario.save()
            # Create corresponding User for Django authentication
            user = User.objects.create_user(username=usuario.correo, email=usuario.correo, password=usuario.contrasenia)
            user.first_name = usuario.nombre
            user.last_name = usuario.apellido
            user.is_staff = False
            user.save()
        return usuario

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo_pago', 'producto']
        widgets = {
            'metodo_pago': forms.Select(attrs={'class': 'form-control','placeholder': 'Nombre de Usuario'}),
            'producto': forms.Select(attrs={'class': 'form-control','placeholder': 'Correo Electronico'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre por favor'}),
            'precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese precio por favor'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese descripcion por favor'}),
        }

class SuscripcionPlataformaForm(forms.ModelForm):
    class Meta:
        model = SuscripcionPlataforma
        fields = ['producto']

class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo electrónico',  widget=forms.EmailInput(attrs={'class': 'form-control'}))
    contrasenia = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Contraseña')
    
