from django.test import TestCase

from geps.models import Docente

def tests(request):
    if 'segunda' in request.POST:
        for x in request.POST:
            print(request.POST['segunda'])

class CheckDocente(TestCase):
    def setUp(self):
        Docente.objects.create(nome='Teste',
                               email='teste.class@dont.com',
                                telefone='(00) 00000-0000',
                                reg_funcional='000000000',
                                data_cadastro='2020-01-01',
                                status=0)
