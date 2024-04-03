# Generated by Django 5.0.4 on 2024-04-03 19:22

import django.db.models.deletion
import geps.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='all_in_one_accessibility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aioa_license_Key', models.CharField(blank=True, default=' ', help_text="<span class='validate_pro'><p>You are currently using Free version which have limited features. </br>Please <a href='https://www.skynettechnologies.com/add-ons/product/all-in-one-accessibility/'>purchase</a> License Key for additional features on the ADA Widget</p></span><script>if(document.querySelector('#id_aioa_license_Key').value != ''){document.querySelector('.validate_pro').style.display='none';} else {document.querySelector('.validate_pro').style.display='block';}</script>", max_length=150, validators=[geps.models.validate_token], verbose_name='License Key')),
                ('aioa_color_code', models.CharField(blank=True, default=' ', help_text='You can cutomize the ADA Widget color. For example: #FF5733', max_length=50, verbose_name='Hex color code')),
                ('aioa_place', models.CharField(blank=True, choices=[('top_left', 'Top left'), ('top_center', 'Top Center'), ('top_right', 'Top Right'), ('middel_left', 'Middle left'), ('middel_right', 'Middle Right'), ('bottom_left', 'Bottom left'), ('bottom_center', 'Bottom Center'), ('bottom_right', 'Bottom Right')], default=('bottom_right', 'Bottom Right'), max_length=100, verbose_name='Where would you like to place the accessibility icon on your site')),
            ],
            options={
                'verbose_name': 'All in One Accessibility Settings',
                'verbose_name_plural': 'All in One Accessibility Settings',
            },
        ),
        migrations.CreateModel(
            name='Cidade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=150)),
                ('senha', models.CharField(max_length=150)),
                ('telefone', models.CharField(max_length=20, null=True)),
                ('reg_funcional', models.CharField(max_length=100)),
                ('data_cadastro', models.DateTimeField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(max_length=2, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instituicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=200, null=True)),
                ('numero', models.CharField(max_length=10, null=True)),
                ('bairro', models.CharField(default='', max_length=50, null=True)),
                ('municipio', models.CharField(max_length=100, null=True)),
                ('estado', models.CharField(max_length=2, null=True)),
                ('cep', models.CharField(max_length=10, null=True)),
                ('email', models.CharField(max_length=150, null=True)),
                ('telefone', models.CharField(max_length=20, null=True)),
                ('nome_responsavel', models.CharField(max_length=100, null=True)),
                ('email_responsavel', models.CharField(max_length=150, null=True)),
                ('telefone_responsavel', models.CharField(max_length=20, null=True)),
                ('senha', models.CharField(default='', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='RegiaoMetropolitana',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RegiaoMetropolitana', models.CharField(max_length=100, null=True, unique=True)),
            ],
            options={
                'ordering': ['RegiaoMetropolitana'],
            },
        ),
        migrations.CreateModel(
            name='Regioes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regiao', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['regiao'],
            },
        ),
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('cidade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bairros', to='geps.cidade')),
            ],
            options={
                'ordering': ['nome', 'cidade'],
            },
        ),
        migrations.CreateModel(
            name='DisponibilidadeDocente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diaSemana', models.CharField(choices=[('Segunda-Feira', 'seg'), ('Terça-Feira', 'ter'), ('Quarta-Feira', 'qua'), ('Quinta-Feira', 'qui'), ('Sexta-Feira', 'sex')], max_length=20)),
                ('periodo', models.CharField(choices=[('Manhã', 'manha'), ('Tarde', 'tarde'), ('Noite', 'noite')], max_length=20)),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.docente')),
            ],
        ),
        migrations.CreateModel(
            name='DisponibilidadeBairro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bairro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.bairro')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.docente')),
            ],
        ),
        migrations.AddField(
            model_name='cidade',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cidades', to='geps.estado'),
        ),
        migrations.CreateModel(
            name='Demanda',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diaSemana', models.CharField(choices=[('Segunda-Feira', 'seg'), ('Terça-Feira', 'ter'), ('Quarta-Feira', 'qua'), ('Quinta-Feira', 'qui'), ('Sexta-Feira', 'sex')], max_length=20)),
                ('periodo', models.CharField(choices=[('Manhã', 'manha'), ('Tarde', 'tarde'), ('Noite', 'noite')], max_length=20)),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.instituicao')),
            ],
        ),
        migrations.AddField(
            model_name='cidade',
            name='regmet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='regiao', to='geps.regiaometropolitana'),
        ),
        migrations.CreateModel(
            name='DisponibilidadeRegiao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.docente')),
                ('regiao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geps.regioes')),
            ],
        ),
        migrations.AddConstraint(
            model_name='disponibilidadebairro',
            constraint=models.UniqueConstraint(fields=('docente', 'bairro'), name='docente_bairro'),
        ),
        migrations.AddConstraint(
            model_name='cidade',
            constraint=models.UniqueConstraint(fields=('nome', 'estado', 'regmet'), name='CidadeUnica'),
        ),
        migrations.AddConstraint(
            model_name='disponibilidaderegiao',
            constraint=models.UniqueConstraint(fields=('docente', 'regiao'), name='docente_regiao'),
        ),
    ]
