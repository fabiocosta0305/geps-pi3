import datetime
import hashlib

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from geps.models import Docente, Instituicao
from geps.utils.funcoes import checkGroup, checkEmail


# Pagina Inicial do sistema
def home(request):
    return render(request, 'home.html')


# Formulário de Cadastro de Usuario (Docentes)
def cadUser(request):
    return render(request, 'cadUser.html')


# Validacoes e insercao do usuario
def insertUser(request):
    data = {}
    # Validação de nome de usuario
    if len(request.POST['name']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
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
        user = User.objects.create_user(request.POST['name'], request.POST['email'], request.POST['password'])
        user.save()
        now = datetime.datetime.utcnow()
        passwd = hashlib.md5()
        passwd.update(b"{request.POST['password']}")
        docente = Docente(
            nome=request.POST['name'],
            email=request.POST['email'],
            senha=passwd.hexdigest(),
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
    # Validação de nome da instituicao
    if len(request.POST['name']) == 0:
        data['msg'] = 'O Nome é obrigatório!'
        data['class'] = 'alert-danger'
        return render(request, 'cadInstituicao.html', data)
    # Validacao do nome do responsavel
    if len(request.POST['name_resp']) == 0:
        data['msg'] = 'O Nome do Responsável é obrigatório!'
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

    else:
        # Validação de nome de usuario ja cadastrado
        if User.objects.filter(username=request.POST['name']).exists():
            data['msg'] = 'Instituição já cadastrada!'
            data['class'] = 'alert-danger'
            return render(request, 'cadInstituicao.html', data)
        # Inserção da Instituicao
        user = User.objects.create_user(request.POST['name_resp'], request.POST['email_resp'], request.POST['password'])
        user.save()
        now = datetime.datetime.utcnow()
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
            nome_responsavel=request.POST['name_resp'],
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
        if checkGroup(user, "Instituicao"):
            data['instituicao'] = True
        return render(request, 'dashboard/home.html', data)
    else:
        data['msg'] = 'Usuário ou Senha inválidos!'
        data['class'] = 'alert-danger'
        return render(request, 'loginUser.html', data)


# Página inicial do dashboard
def dashboard(request):
    return render(request, 'dashboard/home.html')


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
    if request.POST['password'] != request.POST['password-conf']:
        data['msg'] = 'As Senhas devem ser iguais!'
        data['class'] = 'alert-danger'
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
