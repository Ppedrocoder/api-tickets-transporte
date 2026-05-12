from django.db import models

# Create your models here.

class Municipio(models.Model):
    nome = models.CharField(max_length=120)
    uf = models.CharField(max_length=2)
    endereco_sede = models.CharField(max_length=200, blank=True)
    ativo = models.BooleanField(default=True)

class EmpresaTransporte(models.Model):
    razao_social = models.CharField(max_length=200)
    nome_fantasia = models.CharField(max_length=150, blank=True)
    cnpj = models.CharField(max_length=18, unique=True)
    endereco = models.CharField(max_length=200, blank=True)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, related_name='empresas')
class Usuario(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, unique=True)
    endereco = models.CharField(max_length=200, blank=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
class TipoTicket(models.Model):
    CHOICES = [
        ('avulso', 'avulso'),
        ('diario', 'diario'),
        ('semanal', 'semanal'),
        ('mensal', 'mensal'),
        ('anual', 'anual'),
    ]
    nome = models.CharField(max_length=100, choices=CHOICES)
    descricao = models.TextField(blank=True)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_dias = models.PositiveSmallIntegerField()
    janela_integracao_minutos = models.PositiveSmallIntegerField(default=60)
    ativo = models.BooleanField(default=True)

class Ticket(models.Model):
    CHOICES = [
        ('ativo', 'ativo'),
        ('expirado', 'expirado'),
        ('cancelado', 'cancelado'),
        ('consumido', 'consumido'),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='tickets')
    tipo = models.ForeignKey(TipoTicket, on_delete=models.PROTECT, related_name='tickets')
    data_compra = models.DateTimeField(auto_now_add=True)
    valor_pago = models.DecimalField(max_digits=8, decimal_places=2)
    data_validade = models.DateTimeField()
    status = models.CharField(max_length=20, choices=CHOICES, default='ativo')

class Transporte(models.Model):
    CHOICES = [
        ('parada', 'parada'),
        ('onibus', 'onibus'),
        ('trem', 'trem'),
    ]
    identificacao = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50, choices=CHOICES)
    nome = models.CharField(max_length=150)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    empresa = models.ForeignKey(EmpresaTransporte, on_delete=models.PROTECT, related_name='transportes')
    ativo = models.BooleanField(default=True)

class Validador(models.Model):
    CHOICES = [
        ('cartao', 'cartao'),
        ('celular', 'celular'),
    ]
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=50, choices=CHOICES)
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, related_name='validadores', null=True, blank=True)
    data_instalacao = models.DateTimeField()
    ativo = models.BooleanField(default=True)
class Validacao(models.Model):
    tiket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name='validacoes')
    validador = models.ForeignKey(Validador, on_delete=models.PROTECT, related_name='validacoes')
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, related_name='validacoes')
    data_hora = models.DateTimeField(auto_now_add=True)
    dentro_janela_integracao = models.BooleanField(default=False)
    valor_debitado = models.DecimalField(max_digits=8, decimal_places=2, default=0)