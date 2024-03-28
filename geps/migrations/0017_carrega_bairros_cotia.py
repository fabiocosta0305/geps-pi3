# Generated by Django 3.2.12 on 2023-05-19 13:51

from django.db import migrations
import os

def load_initial_data(apps, schema_editor):
    # get our model
    # get_model(appname, modelname)
    cidade_model = apps.get_model('geps', 'Cidade')
    bairro_model = apps.get_model('geps', 'Bairro')

    # Modifique a lista abaixo como necessário para sua localidade    

    cidade_id=cidade_model.objects.get(nome = "Cotia", estado__sigla='SP')
    
    # Inclua na lista todos os bairros necessários
    this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source_data'))
    bairros=open(this_dir + '/bairros_cotia.txt')
    
    for i in bairros.readlines():    
        bairro_model.objects.get_or_create(nome = i.rstrip(), cidade_id = cidade_id.pk)

def clean_reverse_data(apps, schema_editor):
    cidade_model = apps.get_model('geps', 'Cidade')
    bairro_model = apps.get_model('geps', 'Bairro')
    cidade_id=cidade_model.objects.get(nome = "Cotia", estado__sigla='SP')
    bairro_model.objects.all().filter(cidade_id=cidade_id.pk).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('geps', '0016_carrega_bairros_sa'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, clean_reverse_data),        
    ]