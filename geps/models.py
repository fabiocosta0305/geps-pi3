from django.db import models
from model_utils import Choices
from django.core.exceptions import ValidationError

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


# Criando uma classe para as Cidades
class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return self.nome + ' - ' + self.estado.sigla


# Criando uma classe para os Bairros
class Bairro(models.Model):
    objects = None
    nome = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='bairros')

    def __str__(self):
        return self.nome + ' - ' + self.cidade.nome

    class Meta:
        ordering = ['nome']


class Regioes(models.Model):
    regiao = models.CharField(max_length=50)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='regiao')

    def _str_(self):
        return self.nome + ' - ' + self.cidade.nome

    class Meta:
        ordering = ['regiao']


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
        
# Criando uma classe para all_in_one_accessibility
# ------------------------------------------------
aioa_SELECT_CHOICE = [('top_left','Top left'),
      ('top_center','Top Center'),
      ('top_right','Top Right'),
      ('middel_left','Middle left'),
      ('middel_right','Middle Right'),
      ('bottom_left','Bottom left'),
      ('bottom_center','Bottom Center'),
      ('bottom_right','Bottom Right')]
def validate_token(value):
    if value is not None:
        pass
    else:
        raise ValidationError("This field accepts mail id of google only")

aioa_NOTE = "<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span><script>if(document.querySelector('#id_aioa_license_Key').value != ''){document.querySelector('.validate_pro').style.display='none';} else {document.querySelector('.validate_pro').style.display='block';}</script>"

class all_in_one_accessibility(models.Model):
    aioa_license_Key = models.CharField(max_length=150,blank=True,validators=[validate_token],default=' ',verbose_name='License Key',help_text=aioa_NOTE)
    aioa_color_code = models.CharField(max_length=50,blank=True,default=' ',verbose_name ='Hex color code',help_text='You can cutomize the ADA Widget color. For example: #FF5733')
    aioa_place = models.CharField(max_length=100,blank=True,choices=aioa_SELECT_CHOICE,default=('bottom_right','Bottom Right'),verbose_name='Where would you like to place the accessibility icon on your site')

    def __str__(self):

        return '{}, {}, {}'.format(self.aioa_place,self.aioa_color_code, self.aioa_license_Key)

    class Meta:
        verbose_name = 'All in One Accessibility Settings'
        verbose_name_plural = 'All in One Accessibility Settings'
