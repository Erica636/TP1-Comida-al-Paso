# Comida al Paso - API REST

API REST desarrollada con Django para gestionar productos de un negocio gastronómico. Incluye autenticación JWT y está dockerizada.

## Tecnologías
- Python 3.12
- Django 5.x
- Django REST Framework
- PostgreSQL
- Docker
- JWT (SimpleJWT)

## Instalación

1. Clonar el repo:
```bash
git clone [tu-repo]
cd comida_al_paso_project
```

2. Levantar con Docker:
```bash
docker-compose up --build
```

El servidor va a estar en `http://localhost:8000`

## Endpoints principales

**Públicos:**
- `GET /api/productos/` - Listar productos
- `GET /api/categorias/` - Listar categorías

**Protegidos (requieren JWT):**
- `POST /api/productos/` - Crear producto
- `PUT /api/productos/{id}/` - Actualizar
- `DELETE /api/productos/{id}/` - Eliminar

## Autenticación

Para obtener un token:
```bash
POST /api/token/
{
  "username": "admin",
  "password": "tu_password"
}
```

Usar el token en las peticiones:
```bash
Authorization: Bearer [tu-token]
```

## Comandos útiles
```bash
# Ver logs
docker-compose logs -f web

# Detener contenedores
docker-compose down

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

## Notas

- El proyecto cumple con los requisitos de seguridad OWASP
- Incluye validaciones en los serializers
- Los logs se guardan en la carpeta `logs/`
- DEBUG está en False para producción

**Autor:** Erica Ansaloni