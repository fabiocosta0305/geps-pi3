from django.forms import ModelForm
from geps.models import Docente

# Create the form class.
class DocenteForm(ModelForm):
    class Meta:
        model = Docente
        fields = ['nome', 'email', 'senha', 'telefone', 'reg_funcional']