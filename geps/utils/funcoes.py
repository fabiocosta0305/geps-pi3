import re
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import django.contrib.auth.password_validation as validation
from django.shortcuts import render

regex = '([a-zA-Z0-9_.+-]+)@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9_.+-]'


# Função para validar email
def checkEmail(email):
    result = False
    if re.search(regex, email):
        result = True
    return result


# Função para validar Grupo de Usuario
def checkGroup(usuario, grupo):
    users_in_group = Group.objects.get(id=grupo).user_set.all()
    if usuario in users_in_group:
        return True
    else:
        return False


# Enviando Email
def enviandoEmail(request):
    data = {}
    data['instituicao'] = True
    from_email = settings.EMAIL_HOST_USER
    send_mail(request.GET.get('assunto'), request.GET.get('mensagem'), from_email, [request.GET.get('email')], fail_silently=True)
    return render(request, 'dashboard/pesquisaDocente.html', data)


# Validando Senha Usuário
def checkPassword(user, password):
    messages = {"invalid_password": None,
                "password_validations": None,
                "success": None,
                "other": None,
                "mismatched": None
                }
    try:
        validation.validate_password(password, user)
        messages["success"] = "OK"
    except ValidationError as val_err:
        messages["password_validations"] = val_err.messages
    return messages
