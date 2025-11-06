from rest_framework import serializers
from .models import Categoria, Producto


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='categoria.nombre')
    descripcion = serializers.CharField(
        source='categoria.descripcion', 
        read_only=True
    )
    
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'descripcion']


class ProductoCreateSerializer(serializers.Serializer):
    nombre_producto = serializers.CharField(max_length=200)
    nombre_categoria = serializers.CharField(max_length=100)
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField(default=0)
    
    def create(self, validated_data):
        nombre_producto = validated_data['nombre_producto']
        nombre_categoria = validated_data['nombre_categoria']
        precio = validated_data['precio']
        stock = validated_data.get('stock', 0)
        
        try:
            categoria = Categoria.objects.get(nombre__iexact=nombre_categoria)
        except Categoria.DoesNotExist:
            raise serializers.ValidationError(
                {'error': 'Categoría no encontrada'}
            )
        
        producto = Producto.objects.create(
            nombre=nombre_producto,
            categoria=categoria,
            precio=precio,
            stock=stock
        )
        return producto