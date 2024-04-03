# Generated by Django 4.2.6 on 2024-03-19 12:05

from django.db import migrations
# import csv
import duckdb, os
# from geps.models import Estado

# TODO
def load_data(apps,schema_editor):
    # pass
    estado_model=apps.get_model('geps', 'Estado')
    this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source_data'))
    myduck=duckdb.connect(this_dir + "/cidades_completo.duckdb")
    estados=myduck.execute("select distinct Estado from cidades").fetchall()
    for estado in estados:
        # print(estado[0])  # depuração de inserção
        estado_model.objects.get_or_create(sigla = estado[0])

# TODO
def empty_data(apps,schema_editor):
    estado_model = apps.get_model('geps', 'Estado')
    estado_model.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('geps', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_data,empty_data)
    ]
