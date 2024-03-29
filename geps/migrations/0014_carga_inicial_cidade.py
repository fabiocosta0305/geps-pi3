# Generated by Django 4.2.6 on 2024-03-19 12:05

from django.db import migrations
# import csv
import duckdb, os
# from geps.models import Estado

# TODO
def load_data(apps,schema_editor):
    # pass
    cidade_model=apps.get_model('geps', 'Cidade')
    estado_model=apps.get_model('geps', 'Estado')
    regmet_model=apps.get_model('geps', 'RegiaoMetropolitana')
    this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'source_data'))
    myduck=duckdb.connect(this_dir + "/cidades_completo.duckdb")
    #  
    # ATENÇÃO: case use o código abaixo para carga de todas as cidades do país, 
    #          comente as linhas 23 a 25 e descomente as linhas 22, 29 e 30
    #
    # Utilize os códigos das linhas 23 a 25 se necessário devido a erros de max_questions do MySQL ou similares
    # 
    # cidades=myduck.execute("select Estado,RegiaoMetropolitana,Cidade,lat,lon from cidades").fetchall()
    cidades=myduck.execute("select Estado,RegiaoMetropolitana,Cidade,lat,lon from cidades where Estado='SP' and RegiaoMetropolitana='Metropolitana de São Paulo'").fetchall()
    estado_instancia = estado_model.objects.get(sigla = 'SP')
    regmet_instancia = regmet_model.objects.get(RegiaoMetropolitana = 'Metropolitana de São Paulo')
    for cidade in cidades:
        estado,regmet,cidade,lat,lon=cidade
        #
        # estado_instancia = estado_model.objects.get(sigla = estado)
        # regmet_instancia = regmet_model.objects.get(RegiaoMetropolitana = regmet)
        print(cidade)  # depuração de inserção
        cidade_model.objects.get_or_create(
                nome=cidade,
                regmet = regmet_instancia,
                estado = estado_instancia,
                lat = lat,
                lng = lon
            )

# TODO
def empty_data(apps,schema_editor):
    cidade_model=apps.get_model('geps', 'Cidade')
    cidade_model.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('geps', '0013_carga_inicial_regmet'),
    ]

    operations = [
        migrations.RunPython(load_data,empty_data)
    ]
