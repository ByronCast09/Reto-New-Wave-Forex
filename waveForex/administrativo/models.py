from django.db import models
from django.utils import timezone
from datetime import timedelta

class Usuario(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    contrasenia = models.CharField(max_length=30)
    correo = models.EmailField(max_length=254, unique=True)
    telefono = models.CharField(max_length=30)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s - %s- %s - %s - %s - %s" % (self.nombre,
                                                self.apellido,
                                                self.contrasenia,
                                                self.correo,
                                                self.telefono,
                                                self.fecha_registro)
                                                
class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.FloatField()
    descripcion = models.CharField(max_length=250)

    def __str__(self):
        return "%s - %.2f - %s" % (self.nombre, 
                                        self.precio,
                                        self.descripcion)

class Pago(models.Model):
    OPCIONES_PAGO = (
        ('paypal', 'PayPal'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia Bancaria'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='pagos')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    total_pagar = models.FloatField()
    metodo_pago = models.CharField(max_length=20, choices=OPCIONES_PAGO)

    def save(self, *args, **kwargs):
        if not self.total_pagar:
            self.total_pagar = self.producto.precio
        super().save(*args, **kwargs)

    def __str__(self):
            return "%s - %.2f - %s" % (self.fecha_pago, 
                                                self.total_pagar,
                                                self.metodo_pago)

class SuscripcionPlataforma(models.Model):
    OPCIONES_ESTADO = (
        ('activo', 'Suscripción activa'),
        ('no_activo', 'Suscripción no activa'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='suscripciones')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='suscripciones')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=OPCIONES_ESTADO)

    def __str__(self):
            return "%s - %s - %s" % (self.fecha_inicio, 
                                                    self.fecha_fin,
                                                    self.estado)

class AccesoPlataforma(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='accesos')
    zoom = models.BooleanField(default=False)
    discord = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)
    google_classroom = models.BooleanField(default= False)
    youtube = models.BooleanField(default=False)

    def __str__(self):
        return f"Usuario: {self.usuario.nombre} - Zoom: {self.zoom} - Discord: {self.discord} - WhatsApp: {self.whatsapp} - Google Classroom: {self.google_classroom} - YouTube: {self.youtube}"

# class Video(models.Model):
#     titulo = models.CharField(max_length=200)
#     url = models.URLField(max_length=200)
#     usuarios = models.ManyToManyField(Usuario, through='UsuarioVideo')

#     def __str__(self):
#             return "%s - %s" % (self.titulo, 
#                                     self.url)


# class UsuarioVideo(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
#     video = models.ForeignKey(Video, on_delete=models.CASCADE)
#     acceso = models.BooleanField(default=False)

#     def __str__(self):
#             return "%s - %s - %s" % (self.usuario, 
#                                             self.video,
#                                             self.acceso)