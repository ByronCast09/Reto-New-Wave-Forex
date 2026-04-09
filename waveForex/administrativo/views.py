from django.shortcuts import render, redirect ,get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from .models import Usuario, Producto, Pago, SuscripcionPlataforma, AccesoPlataforma
from .forms import UsuarioForm, PagoForm, ProductoForm, SuscripcionPlataformaForm, LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from googleapiclient.discovery import build
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .functions import generateAccessToken, create_order, capture_order

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

API_KEY = 'AIzaSyBDGm91im-ZPfLFHiklsJIRYa8Jb3NeBQ4'

def get_youtube_service():
    return build('youtube', 'v3', developerKey=API_KEY)

def get_playlist_videos(playlist_id):
    youtube = get_youtube_service()
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    return response['items']


def index(request):
   
    return render(request, 'index.html')

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    usuarios_con_pagos = []

    for u in usuarios:
        pagos = Pago.objects.filter(usuario=u)
        suscripcion_activa = False
        if pagos.exists():
            ultimo_pago = pagos.latest('fecha_pago')
            if timezone.now() - ultimo_pago.fecha_pago < timedelta(days=2):
                suscripcion_activa = True
        
        usuarios_con_pagos.append({
            'usuario': u,
            'suscripcion_activa': suscripcion_activa,
        })

    informacion_template = {'usuarios_con_pagos': usuarios_con_pagos, 'numero_usuarios': len(usuarios)}
    return render(request, 'listar_usuarios.html', informacion_template)


def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            # Login the user after registration
            user = authenticate(username=usuario.correo, password=form.cleaned_data['contrasenia'])
            if user is not None:
                login(request, user)
            return redirect('/', usuario_id=usuario.id)
    else:
        form = UsuarioForm()
    return render(request, 'registrar_usuario.html', {'form': form})


def ingreso(request):

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.data.get("username")
            raw_password = form.data.get("password")
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                
                # Redireccion de administrador vs usuario normal
                if user.is_superuser:
                    return redirect('listar_usuarios')
                else:
                    return redirect(perfil_usuario)
    else:
        form = AuthenticationForm()

    informacion_template = {'form': form}
    return render(request, 'registration/login.html', informacion_template)

def logout_view(request):
    logout(request)
    messages.info(request, "Has salido del sistema")
    return redirect(index)


def editar_usuario(request, id):
    """
    """
    usuario = Usuario.objects.get(pk=id)
    if request.method=='POST':
        formulario = UsuarioForm(request.POST, instance=usuario)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_usuarios')
    else:
        formulario = UsuarioForm(instance=usuario)
    diccionario = {'formulario': formulario}

    return render(request, 'editar_usuario.html', diccionario)

def obtener_usuario(request, id):
    usuario = Usuario.objects.get(pk=id)
    
    pagos = Pago.objects.filter(usuario=usuario)
    
    informacion_template = {'usuario': usuario, 'pagos': pagos}
    
    return render(request, 'obtener_usuario.html', informacion_template)

def realizar_pago(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            try:
                pago = form.save(commit=False)
                pago.usuario = usuario
                producto = pago.producto
                if producto:
                    pago.total_pagar = producto.precio
                else:
                    return render(request, 'realizar_pago.html', {'form': form, 'usuario': usuario, 'error': 'Producto no encontrado'})
                
                pago.save()
                return redirect('crear_suscripcion', usuario_id=usuario.id, producto_id=pago.producto.id, pago_id=pago.id)
            except Exception as e:
                return render(request, 'realizar_pago.html', {'form': form, 'usuario': usuario, 'error': str(e)})
    else:
        form = PagoForm()
    
    return render(request, 'realizar_pago.html', {'form': form, 'usuario': usuario})





def crear_suscripcion(request):
    # usuario_id = request.GET.get('usuario_id')
    # producto_id = request.GET.get('producto_id')
    # pago_id = request.GET.get('pago_id')

    # if not usuario_id or not producto_id or not pago_id:
    #     # Manejar el caso en que los parámetros no están presentes
    #     return render(request, 'error.html', {'mensaje': 'Parámetros insuficientes para crear suscripción'})

    # usuario = Usuario.objects.get(id=usuario_id)
    # producto = Producto.objects.get(id=producto_id)
    # pago = Pago.objects.get(id=pago_id)
    
    # fecha_inicio = timezone.now()
    # fecha_fin = fecha_inicio + timedelta(days=30)  # Suscripción válida por 30 días
    
    # suscripcion = SuscripcionPlataforma.objects.create(
    #     usuario=usuario,
    #     producto=producto,
    #     fecha_inicio=fecha_inicio,
    #     fecha_fin=fecha_fin,
    #     estado='Activo'
    # )
    
    # AccesoPlataforma.objects.create(
    #     usuario=usuario,
    #     zoom=True,
    #     discord=True,
    #     whatsapp=True,
    #     google_classroom=True,
    #     youtube=True
    # )
    
    return render(request, 'suscripcion_exitosa.html')
    return render(request, 'suscripcion_exitosa.html', {'usuario': usuario, 'producto': producto, 'suscripcion': suscripcion, 'pago': pago})


def videos(request):
    playlist_id = 'PLDjtbBXUusIxBDKSesacCWXtzQQAmBnSc'
    video_items = get_playlist_videos(playlist_id)
    videos = [
        {
            'title': item['snippet']['title'],
            'videoId': item['snippet']['resourceId']['videoId'],
            'thumbnail_url': item['snippet']['thumbnails']['high']['url'],
            'publishedAt': item['snippet']['publishedAt'],  # Fecha de publicación
            'author': item['snippet']['channelTitle']
        }
        for item in video_items
    ]
    return render(request, 'indexusuario.html', {'videos': videos})


def plataformas(request):
    return render(request, 'plataformas.html')

def mentores(request):
    return render(request, 'mentores.html')

def planes(request):
    return render(request, 'planes.html')

def perfil_usuario(request):
    usuario = request.user
    
    # Redirigir si es administrador
    if usuario.is_superuser:
        return redirect('listar_usuarios')
        
    try:
        usuario_info = Usuario.objects.get(correo=usuario.email)
    except Usuario.DoesNotExist:
        return redirect('index')
        
    pagos = Pago.objects.filter(usuario=usuario_info).order_by('-fecha_pago')
    
    tiene_pagos = pagos.exists()
    
    if tiene_pagos:
        ultimo_pago = pagos.first().fecha_pago.date()  # Asegurarse de que sea un objeto date
        dias_suscripcion = 30  # Duración de la suscripción en días
        fecha_actual = timezone.now().date()
        dias_restantes = (ultimo_pago + timedelta(days=dias_suscripcion) - fecha_actual).days
    else:
        ultimo_pago = None
        dias_restantes = None
    
    context = {
        'usuario': usuario_info,
        'pagos': pagos,
        'tiene_pagos': tiene_pagos,
        'ultimo_pago': ultimo_pago,
        'dias_restantes': dias_restantes,
    }
    
    return render(request, 'perfilusuario.html', context)

def listar_productos(request):
    productos = Producto.objects.all()

    informacion_template = {'productos': productos, 'numero_productos': len(productos)}
    return render(request, 'listar_productos.html', informacion_template)

def crear_producto(request):
    """
    """
    if request.method=='POST':
        formulario = ProductoForm(request.POST)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save() # se guarda en la base de datos
            return redirect('listar_productos')
    else:
        formulario = ProductoForm()
    diccionario = {'formulario': formulario}

    return render(request, 'crear_producto.html', diccionario)
    
def editar_producto(request, id):
    """
    """
    producto = Producto.objects.get(pk=id)
    if request.method=='POST':
        formulario = ProductoForm(request.POST, instance=producto)
        print(formulario.errors)
        if formulario.is_valid():
            formulario.save()
            return redirect('listar_productos')
    else:
        formulario = ProductoForm(instance=producto)
    diccionario = {'formulario': formulario}

    return render(request, 'editar_producto.html', diccionario)

def eliminar_producto(request, id):
    """
    """
    producto = Producto.objects.get(pk=id)
    producto.delete()
    return redirect('listar_productos.html')

def obtener_membresias(request, id):
    producto = Producto.objects.get(pk=id)
    un_mes_atras = datetime.now() - timedelta(days=30)
    pagos = Pago.objects.filter(producto=producto, fecha_pago__gte=un_mes_atras)

    informacion_template = {
        'pagos': pagos,
        'producto': producto,
    }

    return render(request, 'obtener_membresias.html', informacion_template)


class CrearOrden(APIView):
    def post(self, request):
        print("Datos recibidos:", request.data)  # Imprime los datos recibidos
        try:
            producto_id = request.data.get('producto_id')
            if not producto_id:
                return Response({'error': 'Producto ID es requerido'}, status=status.HTTP_400_BAD_REQUEST)

            producto = Producto.objects.get(id=producto_id)
            order = create_order(producto)
            if 'error' in order:
                return Response(order, status=status.HTTP_400_BAD_REQUEST)

            return Response(order, status=status.HTTP_200_OK)
        except Producto.DoesNotExist:
            return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CapturarOrdenPaypal(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            order_id = self.kwargs['order_id']
            response = capture_order(order_id)
            
            if response.get('status') == 'COMPLETED':

                producto_id = request.data.get('producto_id')
                usuario_id = request.data.get('usuario_id')
                
                producto = Producto.objects.get(id=producto_id)
                usuario = Usuario.objects.get(id=usuario_id)
                
                Pago.objects.create(
                    usuario=usuario,
                    producto=producto,
                    total_pagar=producto.precio,
                    metodo_pago='paypal'
                )
                
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Error al capturar la orden'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'error': 'Error en la captura'}, status=status.HTTP_400_BAD_REQUEST)

