from .models import *
from rest_framework import serializers


class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

class EmpresaTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpresaTransporte
        fields = '__all__'
    
    municipio_nome = serializers.CharField(source='municipio.nome', read_only=True)

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
    saldo = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

class TipoTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoTicket
        fields = '__all__'
    
    nome_display = serializers.CharField(source='get_nome_display', read_only=True)