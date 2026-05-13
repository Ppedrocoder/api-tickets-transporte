"""
URL configuration for tickets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from logica.views import *


router = DefaultRouter()
router.register(r'municipios', MunicipioViewSet, basename='municipio')
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
schema_view = get_schema_view(
    openapi.Info(
            title="API de Tickets de Transporte",
            default_version='v1',
            description="API para gerenciamento de tickets de transporte público",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="rpedroricardo87@gmail.com"),
            license=openapi.License(name="MIT License"),
        ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Rota para baixar o arquivo JSON ou YAML puro da especificação
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Rota para a interface visual do Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Rota para a interface visual alternativa do ReDoc
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
