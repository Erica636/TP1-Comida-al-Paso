from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')

urlpatterns = [
    path('', views.api_home, name='api-home'),
    path('test', views.test_api, name='test-api'),
    path('', include(router.urls)),
    path('productos', views.productos_list, name='productos-list'),
    path('productos/', views.productos_list, name='productos-list-slash'),
    re_path(r'^productos/(?P<categoria_nombre>[^/]+)$', views.productos_por_categoria, name='productos-por-categoria'),
]