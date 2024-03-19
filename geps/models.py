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
            ('Segunda-Feira','seg'), ('Terça-Feira','ter'), ('Quarta-Feira','qua'),('Quinta-Feira','qui'),('Sexta-Feira','sex')
        )
    Periodo = Choices (
            ('Manhã','manha'), ('Tarde','tarde'), ('Noite','noite')
        )
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    diaSemana = models.CharField(max_length=20, choices=DiaSemana)
    periodo = models.CharField(max_length=20, choices=Periodo)

    def checkbox(self):
        checkDia={'Segunda-Feira': 'seg', 'Terça-Feira':'ter', 'Quarta-Feira':'qua','Quinta-Feira':'qui','Sexta-Feira':'sex'}
        checkPeriodo={'Manhã':'manha', 'Tarde':'tarde', 'Noite':'noite'}
        return self.get_diaSemana_display()+'_'+self.get_periodo_display()


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
            ('Segunda-Feira','seg'), ('Terça-Feira','ter'), ('Quarta-Feira','qua'),('Quinta-Feira','qui'),('Sexta-Feira','sex')
        )
    Periodo = Choices (
            ('Manhã','manha'), ('Tarde','tarde'), ('Noite','noite')
        )
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    diaSemana = models.CharField(max_length=20, choices=DiaSemana)
    periodo = models.CharField(max_length=20, choices=Periodo)


# Criando uma classe para os Estados
class Estado(models.Model):
    sigla = models.CharField(max_length=2, null=True)

    def __str__(self):
        return self.sigla

class RegiaoMetropolitana(models.Model):
    RegiaoMetropolitana = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.RegiaoMetropolitana
    
    class Meta:
        ordering = ['RegiaoMetropolitana']


# Criando uma classe para as Cidades
class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')
    # regiao = models.ForeignKey(Regioes, on_delete=models.CASCADE, related_name="regiao",null=True)
    regmet = models.ForeignKey(RegiaoMetropolitana, on_delete=models.CASCADE, related_name="regiao",null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.nome + ' - ' + self.estado.sigla


class Regioes(models.Model):
    regiao = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='regiao')

    def _str_(self):
        return self.nome + ' - ' + self.cidade.nome

    class Meta:
        ordering = ['regiao']


# Criando uma classe para os Bairros
class Bairro(models.Model):
    objects = None
    nome = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='bairros')

    def __str__(self):
        return self.nome + ' - ' + self.cidade.nome

    class Meta:
        ordering = ['nome']


class DisponibilidadeRegiao(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    regiao = models.ForeignKey(Regioes, on_delete=models.CASCADE)

    def _str_(self):
        return self.docente.nome + ' - ' + self.regiao.regiao

    class Meta:
        constraints = [ 
                        models.UniqueConstraint(
                            fields=['docente','regiao'],
                            name="docente_regiao"
                        )
                      ]

class DisponibilidadeBairro(models.Model):
    objects = None
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)

    def _str_(self):
        return self.docente.nome + ' - ' + self.regiao.bairro
    
    class Meta:
        constraints = [ 
                        models.UniqueConstraint(
                            fields=['docente','bairro'],
                            name="docente_bairro"
                        )
                      ]