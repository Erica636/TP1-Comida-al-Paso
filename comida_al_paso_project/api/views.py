from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Categoria, Producto
from .serializers import (
    CategoriaSerializer, 
    ProductoSerializer,
    ProductoCreateSerializer
)


@api_view(['GET'])
def api_home(request):
    """Página de inicio de la API"""
    return Response({
        'mensaje': 'Bienvenido a la API de Inventario',
        'version': '1.0.0',
        'endpoints_disponibles': [
            'GET  /api/test - Endpoint de prueba',
            'GET  /api/categorias - Obtener todas las categorías',
            'POST /api/categorias - Crear nueva categoría',
            'GET  /api/productos - Obtener todos los productos',
            'POST /api/productos - Crear nuevo producto',
            'GET  /api/productos/<categoria> - Productos por categoría'
        ],
        'documentacion': 'Envía requests a los endpoints para interactuar con el inventario'
    })


@api_view(['GET'])
def test_api(request):
    """Endpoint de prueba"""
    total_categorias = Categoria.objects.count()
    return Response({
        'mensaje': 'API funcionando correctamente',
        'total_categorias': total_categorias
    })


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def create(self, request, *args, **kwargs):
        nombre = request.data.get('nombre')
        descripcion = request.data.get('descripcion', '')
        
        if not nombre:
            return Response(
                {'error': 'Nombre es requerido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            categoria = Categoria.objects.create(
                nombre=nombre,
                descripcion=descripcion
            )
            serializer = self.get_serializer(categoria)
            return Response({
                'mensaje': 'Categoría creada exitosamente',
                'categoria': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET', 'POST'])
def productos_list(request):
    """Listar todos los productos o crear uno nuevo"""
    if request.method == 'GET':
        productos = Producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        create_serializer = ProductoCreateSerializer(data=request.data)
        
        if not create_serializer.is_valid():
            return Response(
                create_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            producto = create_serializer.save()
            
            return Response({
                'mensaje': 'Producto creado exitosamente',
                'producto': {
                    'nombre': producto.nombre,
                    'categoria': producto.categoria.nombre,
                    'precio': float(producto.precio),
                    'stock': producto.stock
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def productos_por_categoria(request, categoria_nombre):
    """Obtener productos de una categoría específica"""
    productos = Producto.objects.filter(
        categoria__nombre__iexact=categoria_nombre
    )
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)