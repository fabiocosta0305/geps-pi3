from django.db import models
from model_utils import Choices


# Criando classe com campos de Docente
class Docente(models.Model):
    objects = None
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    senha = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, null=True)
    reg_funcional = models.CharField(max_length=100)
    data_cadastro = models.DateTimeField()
    status = models.IntegerField(default=0)


# Criando uma classe representando a disponibilidade dos Docentes
class DisponibilidadeDocente(models.Model):
    objects = None
    DiaSemana = Choices (
            ('Segunda-Feira'), ('Terça-Feira'), ('Quarta-Feira'),('Quinta-Feira'),('Sexta-Feira')
        )
    Periodo = Choices (
            ('Manhã'), ('Tarde'), ('Noite')
        )
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    diaSemana = models.CharField(max_length=20, choices=DiaSemana)
    periodo = models.CharField(max_length=20, choices=Periodo)


# Classe com dos campos da Instituição
class Instituicao(models.Model):
    objects = None
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=200, null=True)
    numero = models.CharField(max_length=10, null=True)
    bairro = models.CharField(max_length=50, null=True, default='')
    municipio = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=2, null=True)
    cep = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=150, null=True)
    telefone = models.CharField(max_length=20, null=True)
    nome_responsavel = models.CharField(max_length=100, null=True)
    email_responsavel = models.CharField(max_length=150, null=True)
    telefone_responsavel = models.CharField(max_length=20, null=True)
    senha = models.CharField(max_length=150, default='')

# Criando uma classe que representa a Demanda por professores
class Demanda(models.Model):
    DiaSemana = Choices (
            ('Segunda-Feira'), ('Terça-Feira'), ('Quarta-Feira'),('Quinta-Feira'),('Sexta-Feira')
        )
    Periodo = Choices (
            ('Manhã'), ('Tarde'), ('Noite')
        )
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    diaSemana = models.CharField(max_length=20, choices=DiaSemana)
    periodo = models.CharField(max_length=20, choices=Periodo)
