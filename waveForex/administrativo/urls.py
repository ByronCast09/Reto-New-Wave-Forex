
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mentores/', views.mentores, name='mentores'),
    path('planes/', views.planes, name='planes'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('pago/<int:usuario_id>/', views.realizar_pago, name='pago'),
    # path('suscripcion/<int:usuario_id>/<int:producto_id>/<int:pago_id>/', views.crear_suscripcion, name='crear_suscripcion'),
    path('suscripcion/', views.crear_suscripcion, name='crear_suscripcion'),
    
    path('administrativo/', views.listar_usuarios, name='listar_usuarios'),
    path('administrativo/productos', views.listar_productos, name='listar_productos'),
    
    path('editar/usuario/<int:id>', views.editar_usuario, name='editar_usuario'),

    path('crear/producto', views.crear_producto, name='crear_producto'),
    path('editar_producto/<int:id>', views.editar_producto, name='editar_producto'),
    path('eliminar/producto/<int:id>', views.eliminar_producto, name='eliminar_producto'),
        
    path('usuario/<int:id>', views.obtener_usuario, name='obtener_usuario'),
    path('membresia/<int:id>', views.obtener_membresias, name='obtener_membresias'),

    path('videos/', views.videos, name='videos'),
     path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('plataformas/', views.plataformas, name='plataformas'),
    path('saliendo/logout/', views.logout_view, name="logout_view"),
    path('entrando/login/', views.ingreso, name="login"),
]