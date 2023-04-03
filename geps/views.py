from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from geps.models import Docente,Instituicao
from geps.utils import funcoes
from geps.forms import DocenteForm

# Pagina Inicial do sistema
def home(request):
    return render(request, 'home.html')


# Formulário de Cadastro de Usuario (Docentes)
def cadUser(request):
    return render(request, 'cadUser.html')

# Formulário de Cadastro da Instituicao
def cadInstituicao(request):
    return render(request, 'cadInstituicao.html')

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
    if not funcoes.checkEmail(request.POST['email']):
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
        Docente.reg_funcional = request.POST['reg_funcional']
        #user.reg_funcional = request.POST['reg_funcional']
        user.save()
        data['msg'] = 'Usuário cadastrado com sucesso!'
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
        return redirect('/dashboard/')
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
    if (request.POST['password'] != request.POST['password-conf']):
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
