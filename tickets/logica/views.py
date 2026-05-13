from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from decimal import Decimal
from .models import *
from .serializers import *

# Create your views here.

class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['uf', 'ativo']
    search_fields = ['nome', 'uf']
    ordering_fields = ['nome', 'uf']

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['email']
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'email']

    @action(detail=True, methods=['post'])
    def recarregar_saldo(self, request, pk=None):
        usuario = self.get_object()
        valor = request.data.get('valor')
        if valor is not None and valor > 0:
            try:
                valor = Decimal(str(valor))
                usuario.saldo += valor
                usuario.save()
                return Response({'status': 'saldo recarregado', 'novo_saldo': str(usuario.saldo)})
            except (ValueError, TypeError):
                return Response({'status': 'valor inválido'}, status=400)
        else:
            return Response({'status': 'valor não fornecido ou inválido'}, status=400)