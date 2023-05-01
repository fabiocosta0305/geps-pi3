import datetime
import hashlib
import json

from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse

from geps.models import Docente, Instituicao, Demanda, DisponibilidadeDocente, Bairro
from geps.utils.funcoes import checkGroup, checkEmail, checkPassword


# Pagina Inicial do sistema
def home(request):
    return render(request, 'home.html')


# Formulário de Cadastro de Usuario (Docentes)
def cadUser(request):
    return render(request, 'cadUser.html')


# Validacoes e insercao do usuario
def insertUser(request):
    data = {}
    data['nome'] = request.POST['nome']
    data['name'] = request.POST['name']
    data['email'] = request.POST['email']
    data['telefone'] = request.POST['telefone']
    data['reg_funcional'] = request.POST['reg_funcional']
    # Validação de nome completo
    if len(request.POST['nome']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validação de nome de usuario
    if len(request.POST['name']) == 0:
        data['msg'] = 'O Nome de Usuário é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validação do telefone do usuario
    if len(request.POST['telefone']) == 0:
        data['msg'] = 'O Telefone é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validacão da senha vazia
    if (len(request.POST['password']) == 0) or (len(request.POST['password-conf']) == 0):
        data['msg'] = 'A Senha é obrigatória!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validação de senhas diferentes
    if request.POST['password'] != request.POST['password-conf']:
        data['msg'] = 'As Senhas devem ser iguais!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validacao de conteudo da senha
    retorno = checkPassword(request.POST['name'], request.POST["password"])
    if retorno['success'] != 'OK' and retorno['password_validations']:
        qtd_erros = len(retorno['password_validations'])
        for erros in range(0, qtd_erros):
            data['msg'] = retorno['password_validations'][erros]
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    # Validacao do email invalido
    if not checkEmail(request.POST['email']):
        data['msg'] = 'Email Inválido!'
        data['class'] = 'alert-danger'
        return render(request, 'cadUser.html', data)
    else:
        # Validação de nome de usuario ja cadastrado
        if User.objects.filter(username=request.POST['name']).exists():
            data['msg'] = 'Usuário já cadastrado!'
            data['class'] = 'alert-danger'
            return render(request, 'cadUser.html', data)
        # Validação de email cadastrado
        if User.objects.filter(email=request.POST['email']).exists():
            data['msg'] = 'Email já cadastrado!'
            data['class'] = 'alert-danger'
            return render(request, 'cadUser.html', data)
        # Validação de Registro funcional

        # Inserção no Usuario
        user = User.objects.create_user(
            username=request.POST['name'],
            email=request.POST['email'],
            password=request.POST['password'],
            first_name=request.POST['nome']
        )
        user.save()
        now = datetime.datetime.utcnow()
        passwd = hashlib.md5()
        passwd.update(b"{request.POST['password']}")
        docente = Docente(
            nome=request.POST['nome'],
            email=request.POST['email'],
            senha=passwd.hexdigest(),
            telefone=request.POST['telefone'],
            reg_funcional=request.POST['reg_funcional'],
            data_cadastro=now.strftime('%Y-%m-%d %H:%M:%S'),
            status=0
        )
        docente.save()
        user_group = Group.objects.get(id=2)
        user.groups.add(user_group)
        data['msg'] = 'Usuário cadastrado com sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'loginUser.html', data)


# Formulário de Cadastro da Instituicao
def cadInstituicao(request):
    return render(request, 'cadInstituicao.html')


# Validacoes e insercao da Instituicao
def insertInst(request):
    data = {}
    data['name'] = request.POST['name']
    data['endereco'] = request.POST['endereco']
    data['numero'] = request.POST['numero']
    data['bairro'] = request.POST['bairro']
    data['cep'] = request.POST['cep']
    data['municipio'] = request.POST['municipio']
    data['uf'] = request.POST['uf']
    data['email_inst'] = request.POST['email_inst']
    data['telefone_inst'] = request.POST['telefone_inst']
    data['nome_resp'] = request.POST['nome_resp']
    data['name_resp'] = request.POST['name_resp']
    data['email_resp'] = request.POST['email_resp']
    data['telefone_resp'] = request.POST['telefone_resp']
    # Validação de nome da instituicao
    if len(request.POST['name']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacao do nome completo do responsavel
    if len(request.POST['nome_resp']) == 0:
        data['msg'] = 'O Nome do Responsável é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacao do nome de usuario do responsavel
    if len(request.POST['name_resp']) == 0:
        data['msg'] = 'O Nome de Usuário do Responsável é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacao do email do responsável
    if not checkEmail(request.POST['email_resp']) or len(request.POST['email_resp']) == 0:
        data['msg'] = 'Email do Responsável Inválido!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacão da senha vazia
    if (len(request.POST['password']) == 0) or (len(request.POST['password-conf']) == 0):
        data['msg'] = 'A Senha é obrigatória!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validação de senhas diferentes
    if request.POST['password'] != request.POST['password-conf']:
        data['msg'] = 'As Senhas devem ser iguais!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacao de conteudo da senha
    retorno = checkPassword(request.POST['name'], request.POST["password"])
    if retorno['success'] != 'OK' and retorno['password_validations']:
        qtd_erros = len(retorno['password_validations'])
        for erros in range(0, qtd_erros):
            data['msg'] = retorno['password_validations'][erros]
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    else:
        # Validação de nome de usuario ja cadastrado
        if Instituicao.objects.filter(nome=request.POST['name']).exists():
            data['msg'] = 'Instituição já cadastrada!'
            data['class'] = 'alert-danger'
            return render(request, 'cadInstituicao.html', data)
        # Validacao do nome do responsavel (username)
        if User.objects.filter(username=request.POST['name_resp']).exists():
            data['msg'] = 'Usuário já cadastrado! (' + request.POST['name_resp'] + ')'
            data['class'] = 'alert-danger'
            return render(request, 'cadInstituicao.html', data)
        # Validacao do email do responsavel
        if User.objects.filter(email=request.POST['email_resp']).exists():
            data['msg'] = 'Email do Usuário já cadastrado! (' + request.POST['email_resp'] + ')'
            data['class'] = 'alert-danger'
            return render(request, 'cadInstituicao.html', data)
        # Inserção da Instituicao
        user = User.objects.create_user(
            username=request.POST['name_resp'],
            email=request.POST['email_resp'],
            password=request.POST['password'],
            first_name=request.POST['nome_resp']
        )
        user.save()
        # now = datetime.datetime.utcnow()
        passwd = hashlib.md5()
        passwd.update(b"{request.POST['password']}")
        instituicao = Instituicao(
            nome=request.POST['name'],
            endereco=request.POST['endereco'],
            numero=request.POST['numero'],
            bairro=request.POST['bairro'],
            municipio=request.POST['municipio'],
            estado=request.POST['uf'],
            cep=request.POST['cep'],
            telefone=request.POST['telefone_inst'],
            email=request.POST['email_inst'],
            nome_responsavel=request.POST['nome_resp'],
            email_responsavel=request.POST['email_resp'],
            telefone_responsavel=request.POST['telefone_resp'],
            senha=passwd.hexdigest(),
        )
        instituicao.save()
        user_group = Group.objects.get(id=1)
        user.groups.add(user_group)
        data['msg'] = 'Instituicão cadastrada com sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'loginUser.html', data)


# Formulário de login
def loginUser(request):
    return render(request, 'loginUser.html')


# Validacao e acesso do login
def validLoginUser(request):
    data = {}
    user = authenticate(username=request.POST['name'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        data['instituicao'] = False
        if checkGroup(user, 1):
            data['instituicao'] = True
        return render(request, 'dashboard/home.html', data)
    else:
        data['msg'] = 'Usuário ou Senha inválidos!'
        data['class'] = 'alert-danger'
        return render(request, 'loginUser.html', data)


# Página inicial do dashboard
def dashboard(request):
    data = {}
    if checkGroup(request.user, 1):
        data['instituicao'] = True
    else:
        data['instituicao'] = False
    return render(request, 'dashboard/home.html', data)


# Logout do sistema
def logouts(request):
    logout(request)
    return redirect('/loginUser/')


# Formulário de troca de senha
def changePassword(request):
    return render(request, 'changePassword.html')


# Alterar a senha do Usuario
def validChangePassword(request):
    data = {}
    user = User.objects.get(email=request.user.email)
    # Valida senhas diferentes
    if request.POST['password'] != request.POST['password-conf']:
        data['msg'] = 'As Senhas devem ser iguais!'
        data['class'] = 'alert-danger'
        return render(request, 'changePassword.html', data)
    # Valida conteudo de senha
    retorno = checkPassword(request.POST['name'], request.POST["password"])
    if retorno['success'] != 'OK' and retorno['password_validations']:
        qtd_erros = len(retorno['password_validations'])
        for erros in range(0, qtd_erros):
            data['msg'] = retorno['password_validations'][erros]
        data['class'] = 'alert-danger'
        return render(request, 'changePassword.html', data)
    else:
        user.set_password(request.POST['password'])
        user.save()
        logout(request)
        data['msg'] = 'Senha Alterada com Sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'loginUser.html', data)


# Página de politica de privacidade
def policy(request):
    return render(request, 'policy.html')


# Pagina de Pesquisa de Docentes
def formPesquisaDocente(request):
    if request.user.is_authenticated:
        data = {}
        nome_instituicao = Instituicao.objects.only('nome').get(email_responsavel=request.user.email).nome
        data['instituicao'] = True
        data['nome_instituicao'] = nome_instituicao
        return render(request, 'dashboard/pesquisaDocente.html', data)
    else:
        return redirect('/dashboard/')


# Busca dados no banco Docente
def pesquisaDocente(request):
    data = {}
    data['instituicao'] = True                      # Envia parametro de grupo
    data['pesquisar'] = request.POST['pesquisar']   # Envia parametro de acionamento do botão pesquisar
    if 'diaSemana' in request.POST:                 # Verifica se algum check ou setado
        dias = request.POST.getlist('diaSemana')    # Pega a lista com todos os checks
        data["checks"] = dias
        # Verifica se algum check de segunda vou setado por periodo
        if 'seg_manha' in dias or 'seg_tarde' in dias or 'seg_noite' in dias:
            if 'seg_manha' in dias:
                periodo_manha = Q(periodo__contains='Manhã')
            else:
                periodo_manha = Q()
            if 'seg_tarde' in dias:
                periodo_tarde = Q(periodo__contains='Tarde')
            else:
                periodo_tarde = Q()
            if 'seg_noite' in dias:
                periodo_noite = Q(periodo__contains='Noite')
            else:
                periodo_noite = Q()
            segunda = Q(diaSemana__contains='Segunda-Feira') & (periodo_manha | periodo_tarde | periodo_noite)
        else:
            segunda = Q()
        # Verifica se algum check de terça vou setado por periodo
        if 'ter_manha' in dias or 'ter_tarde' in dias or 'ter_noite' in dias:
            if 'ter_manha' in dias:
                periodo_manha = Q(periodo__contains='Manhã')
            else:
                periodo_manha = Q()
            if 'ter_tarde' in dias:
                periodo_tarde = Q(periodo__contains='Tarde')
            else:
                periodo_tarde = Q()
            if 'ter_noite' in dias:
                periodo_noite = Q(periodo__contains='Noite')
            else:
                periodo_noite = Q()
            terca = Q(diaSemana__contains='Terca-Feira') & (periodo_manha | periodo_tarde | periodo_noite)
        else:
            terca = Q()
        # Verifica se algum check de quarta vou setado por periodo
        if 'qua_manha' in dias or 'qua_tarde' in dias or 'qua_noite' in dias:
            if 'qua_manha' in dias:
                periodo_manha = Q(periodo__contains='Manhã')
            else:
                periodo_manha = Q()
            if 'qua_tarde' in dias:
                periodo_tarde = Q(periodo__contains='Tarde')
            else:
                periodo_tarde = Q()
            if 'qua_noite' in dias:
                periodo_noite = Q(periodo__contains='Noite')
            else:
                periodo_noite = Q()
            quarta = Q(diaSemana__contains='Quarta-Feira') & (periodo_manha | periodo_tarde | periodo_noite)
        else:
            quarta = Q()
        # Verifica se algum check de quinta vou setado por periodo
        if 'qui_manha' in dias or 'qui_tarde' in dias or 'qui_noite' in dias:
            if 'qui_manha' in dias:
                periodo_manha = Q(periodo__contains='Manhã')
            else:
                periodo_manha = Q()
            if 'qui_tarde' in dias:
                periodo_tarde = Q(periodo__contains='Tarde')
            else:
                periodo_tarde = Q()
            if 'qui_noite' in dias:
                periodo_noite = Q(periodo__contains='Noite')
            else:
                periodo_noite = Q()
            quinta = Q(diaSemana__contains='Quinta-Feira') & (periodo_manha | periodo_tarde | periodo_noite)
        else:
            quinta = Q()
        # Verifica se algum check de sexta vou setado por periodo
        if 'sex_manha' in dias or 'sex_tarde' in dias or 'sex_noite' in dias:
            if 'sex_manha' in dias:
                periodo_manha = Q(periodo__contains='Manhã')
            else:
                periodo_manha = Q()
            if 'sex_tarde' in dias:
                periodo_tarde = Q(periodo__contains='Tarde')
            else:
                periodo_tarde = Q()
            if 'sex_noite' in dias:
                periodo_noite = Q(periodo__contains='Noite')
            else:
                periodo_noite = Q()
            sexta = Q(diaSemana__contains='Sexta-Feira') & (periodo_manha | periodo_tarde | periodo_noite)
        else:
            sexta = Q()
        # Consulta status validacao docente
        data['cons_validacao'] = request.POST['cons_validacao']
        cons_validacao = Q(docente__status=request.POST['cons_validacao'])
        # Busca no banco de acordo com os dados selecionados
        filtro = DisponibilidadeDocente.objects.filter(
            (segunda | terca | quarta | quinta | sexta) & cons_validacao
        ).values('docente__nome').annotate(Count('docente_id'))
        data['dados'] = filtro
        data['nome_instituicao'] = request.POST['nome_instituicao']
    return render(request, 'dashboard/pesquisaDocente.html', data)


# Busca cadastro Docente
def buscaDocente(request):
    if request.POST.get('nome_docente', False):
        data = {}
        filtro = Docente.objects.filter(nome=request.POST['nome_docente'])
        data = serialize("json", filtro)
        return JsonResponse(data, safe=False)


# Atualiza status Docente
def gravaStatusDocente(request):
    if request.POST['nome_docente']:
        data = {}
        data['instituicao'] = True
        sts = 0
        if request.POST['validacao'] == 'nao_validao':
            sts = 0
        elif request.POST['validacao'] == 'validado':
            sts = 1
        elif request.POST['validacao'] == 'bloqueado':
            sts = 2
        Docente.objects.filter(nome=request.POST['nome_docente']).update(status=sts)
        data['msg'] = 'Validação Gravada com sucesso!'
        data['class'] = 'alert-success'
        data['nome_instituicao'] = request.POST['nome_instituicao']
        return render(request, 'dashboard/pesquisaDocente.html', data)


def formDispDocente(request):
    bairros = Bairro.objects.all
    context = {'all_bairros': bairros}
    return render(request, 'dashboard/disponibilidadeDocente.html', context)


def gravaBairrosDocente(request):
    data = {}  # Cria objeto para retorno
    bairros = Bairro.objects.all  # Busca Todos os Bairros para retornar
    data['all_bairros'] = bairros  # Alimenta o objeto com os bairros
    data['instituicao'] = False  # Controle de grupo de usuário
    docente = Docente.objects.only('id').get(email=request.user.email).id  # Captura id do docente
    # Pega todos os checks de dia da semana e grava no banco
    if ('diaSemana' in request.POST) and ('bairros_selecionados' in request.POST):
        # Pega todos os checks de dia da semana e grava no banco
        dias = request.POST.getlist('diaSemana')
        data["checks"] = dias
        if 'seg_manha' in dias or 'seg_tarde' in dias or 'seg_noite' in dias:
            if 'seg_manha' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Segunda-Feira', periodo='Manhã',
                                                                docente_id=docente)
            if 'seg_tarde' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Segunda-Feira', periodo='Tarde',
                                                                docente_id=docente)
            if 'seg_noite' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Segunda-Feira', periodo='Noite',
                                                                docente_id=docente)
        if 'ter_manha' in dias or 'ter_tarde' in dias or 'ter_noite' in dias:
            if 'ter_manha' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Terça-Feira', periodo='Manhã',
                                                                docente_id=docente)
            if 'ter_tarde' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Terça-Feira', periodo='Tarde',
                                                                docente_id=docente)
            if 'ter_noite' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Terça-Feira', periodo='Noite',
                                                                docente_id=docente)
        if 'qua_manha' in dias or 'qua_tarde' in dias or 'qua_noite' in dias:
            if 'qua_manha' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quarta-Feira', periodo='Manhã',
                                                                docente_id=docente)
            if 'qua_tarde' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quarta-Feira', periodo='Tarde',
                                                                docente_id=docente)
            if 'qua_noite' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quarta-Feira', periodo='Noite',
                                                                docente_id=docente)
        if 'qui_manha' in dias or 'qui_tarde' in dias or 'qui_noite' in dias:
            if 'qui_manha' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quinta-Feira', periodo='Manhã',
                                                                docente_id=docente)
            if 'qui_tarde' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quinta-Feira', periodo='Tarde',
                                                                docente_id=docente)
            if 'qui_noite' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Quinta-Feira', periodo='Noite',
                                                                docente_id=docente)
        if 'sex_manha' in dias or 'sex_tarde' in dias or 'sex_noite' in dias:
            if 'sex_manha' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Sexta-Feira', periodo='Manhã',
                                                                docente_id=docente)
            if 'sex_tarde' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Sexta-Feira', periodo='Tarde',
                                                                docente_id=docente)
            if 'sex_noite' in dias:
                DisponibilidadeDocente.objects.update_or_create(diaSemana='Sexta-Feira', periodo='Noite',
                                                                docente_id=docente)
        # Pegar todos os bairros selecionados
        bairros = request.POST.getlist('bairros_selecionados')
        for bairro in bairros:
            print(bairro)
        data['msg'] = 'Dados gravados com Sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'dashboard/disponibilidadeDocente.html', data)
    else:
        data['msg'] = 'Seleção de dia da Semana e Bairro são obrigatórios!'
        data['class'] = 'alert-danger'
        return render(request, 'dashboard/disponibilidadeDocente.html', data)


# Formulário de Edição da Conta do Usuário
def formEditUser(request):
    data = {}
    data['nome'] = request.user.first_name
    data['name'] = request.user.username
    data['email'] = request.user.email
    docente = Docente.objects.get(email=request.user.email)
    data['telefone'] = docente.telefone
    data['reg_funcional'] = docente.reg_funcional
    data['instituicao'] = False
    return render(request, 'editUser.html', data)


# Validações e update do usuario
def updateUser(request):
    data = {}
    data['nome'] = request.POST['nome']
    data['name'] = request.POST['name']
    data['email'] = request.POST['email']
    data['telefone'] = request.POST['telefone']
    data['reg_funcional'] = request.POST['reg_funcional']
    data['instituicao'] = False
    # Validação de nome completo
    if len(request.POST['nome']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'editUser.html', data)
    # Validação de email vazio
    if len(request.POST['email']) == 0:
        data['msg'] = 'O Email é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'editUser.html', data)
    # Validação do telefone do usuario
    if len(request.POST['telefone']) == 0:
        data['msg'] = 'O Telefone é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'editUser.html', data)
    # Validacao do email invalido
    if not checkEmail(request.POST['email']):
        data['msg'] = 'Email Inválido!'
        data['class'] = 'alert-danger'
        return render(request, 'editUser.html', data)
    # Validacao do email caso seja utilizado algum ja cadastrado
    if (request.user.email != request.POST['email']) and (User.objects.filter(email=request.POST['email']).exists()):
        data['msg'] = 'Email Já Cadastrado!'
        data['class'] = 'alert-danger'
        return render(request, 'editUser.html', data)
    else:
        # Update no Usuario
        Docente.objects.filter(email=request.user.email).update(telefone=request.POST['telefone'],
                                                                reg_funcional=request.POST['reg_funcional'],
                                                                nome=request.POST['nome'],
                                                                email=request.POST['email'])
        User.objects.filter(username=request.user.username).update(email=request.POST['email'],
                                                                   first_name=request.POST['nome'])

        data['msg'] = 'Dados Alterados com sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'editUser.html', data)


# Formulário de Exclusão da Conta de Usuário
def formDeleteUser(request):
    data = {}
    data['instituicao'] = False
    return render(request, 'deleteUser.html', data)


# Exclusão da Conta de Usuário
def deleteUser(request):
    userDocente = Docente.objects.get(email=request.user.email)
    userDocente.delete()
    user = User.objects.get(username=request.user.username)
    user.delete()
    return redirect('/home/')


# Formulário de Edição da Instituição
def formEditInst(request):
    data = {}
    data['instituicao'] = True
    dadosInst = Instituicao.objects.get(email_responsavel=request.user.email)
    data['name'] = dadosInst.nome
    data['endereco'] = dadosInst.endereco
    data['numero'] = dadosInst.numero
    data['bairro'] = dadosInst.bairro
    data['cep'] = dadosInst.cep
    data['municipio'] = dadosInst.municipio
    data['uf'] = dadosInst.estado
    data['email_inst'] = dadosInst.email
    data['telefone_inst'] = dadosInst.telefone
    data['nome_resp'] = dadosInst.nome_responsavel
    data['name_resp'] = request.user.username
    data['email_resp'] = dadosInst.email_responsavel
    data['telefone_resp'] = dadosInst.telefone_responsavel
    return render(request, 'editInstituicao.html', data)


# Validações e update Instituicao
def updateInst(request):
    data = {}
    data['instituicao'] = True
    data['name'] = request.POST['name']
    data['endereco'] = request.POST['endereco']
    data['numero'] = request.POST['numero']
    data['bairro'] = request.POST['bairro']
    data['cep'] = request.POST['cep']
    data['municipio'] = request.POST['municipio']
    data['uf'] = request.POST['uf']
    data['email_inst'] = request.POST['email_inst']
    data['telefone_inst'] = request.POST['telefone_inst']
    data['nome_resp'] = request.POST['nome_resp']
    data['name_resp'] = request.POST['name_resp']
    data['email_resp'] = request.POST['email_resp']
    data['telefone_resp'] = request.POST['telefone_resp']
    # Validacao do nome da instituicao
    if len(request.POST['name']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'editInstituicao.html', data)
    # Validacao do nome completo do responsavel
    if len(request.POST['nome_resp']) == 0:
        data['msg'] = 'O Nome do Responsável é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'editInstituicao.html', data)
    # Validacao do email do responsável
    if not checkEmail(request.POST['email_resp']) or len(request.POST['email_resp']) == 0:
        data['msg'] = 'Email do Responsável Inválido!'
        data['class'] = 'alert-danger'
        return render(request, 'editInstituicao.html', data)
    # Validacao do email caso seja utilizado algum ja cadastrado
    if (request.user.email != request.POST['email_resp']) and (User.objects.filter(email=request.POST['email_resp']).exists()):
        data['msg'] = 'Email Já Cadastrado!'
        data['class'] = 'alert-danger'
        return render(request, 'editInstituicao.html', data)
    else:
        # Update Insituicao
        Instituicao.objects.filter(email_responsavel=request.user.email).update(nome=request.POST['name'],
                                                                                endereco=request.POST['endereco'],
                                                                                numero=request.POST['numero'],
                                                                                bairro=request.POST['bairro'],
                                                                                cep=request.POST['cep'],
                                                                                municipio=request.POST['municipio'],
                                                                                estado=request.POST['uf'],
                                                                                email=request.POST['email_inst'],
                                                                                telefone=request.POST['telefone_inst'],
                                                                                nome_responsavel=request.POST['nome_resp'],
                                                                                email_responsavel=request.POST['email_resp'],
                                                                                telefone_responsavel=request.POST['telefone_resp'])
        User.objects.filter(username=request.user.username).update(email=request.POST['email_resp'],
                                                                   first_name=request.POST['nome_resp'])
        data['msg'] = 'Dados Alterados com sucesso!'
        data['class'] = 'alert-success'
        return render(request, 'editInstituicao.html', data)


# Formulário de Exclusão da Conta de Usuário
def formDeleteInst(request):
    data = {}
    data['instituicao'] = True
    dadosInst = Instituicao.objects.get(email_responsavel=request.user.email)
    data['name'] = dadosInst.nome
    data['nome_resp'] = dadosInst.nome_responsavel
    data['name_resp'] = request.user.username
    data['email_resp'] = dadosInst.email_responsavel
    data['telefone_resp'] = dadosInst.telefone_responsavel
    return render(request, 'deleteInst.html', data)


# Exclusão da Conta de Usuário
def deleteInst(request):
    userInst = Instituicao.objects.get(email_responsavel=request.user.email)
    userInst.delete()
    user = User.objects.get(username=request.user.username)
    user.delete()
    return redirect('/home/')
