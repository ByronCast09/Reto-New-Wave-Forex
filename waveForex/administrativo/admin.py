# admin.py
from django.contrib import admin
from .models import Usuario, Producto, Pago, SuscripcionPlataforma, AccesoPlataforma

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido', 'correo', 'telefono','fecha_registro')
    search_fields = ('nombre', 'apellido' ,'correo', 'telefono','fecha_registro')

admin.site.register(Usuario, UsuarioAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion')
    search_fields = ('nombre', 'precio', 'descripcion')

admin.site.register(Producto, ProductoAdmin)

class PagoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'fecha_pago', 'total_pagar', 'metodo_pago')
    search_fields = ('usuario__nombre', 'producto__nombre', 'metodo_pago')
    raw_id_fields = ('usuario', 'producto')

admin.site.register(Pago, PagoAdmin)

class SuscripcionPlataformaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'fecha_inicio', 'fecha_fin', 'estado')
    search_fields = ('usuario__nombre', 'producto__nombre')
    raw_id_fields = ('usuario',)

admin.site.register(SuscripcionPlataforma, SuscripcionPlataformaAdmin)

class AccesoPlataformaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'zoom', 'discord', 'whatsapp', 'google_classroom', 'youtube')
    search_fields = ('usuario__nombre',)
    raw_id_fields = ('usuario',)

admin.site.register(AccesoPlataforma, AccesoPlataformaAdmin)

# class VideoAdmin(admin.ModelAdmin):
#     list_display = ('titulo', 'url')
#     search_fields = ('titulo',)

# admin.site.register(Video, VideoAdmin)

# class UsuarioVideoAdmin(admin.ModelAdmin):
#     list_display = ('usuario', 'video', 'acceso')
#     search_fields = ('usuario__nombre', 'video__titulo')

# admin.site.register(UsuarioVideo, UsuarioVideoAdmin)
