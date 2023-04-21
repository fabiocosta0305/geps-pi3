import re
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.core import exceptions
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import django.contrib.auth.password_validation as validation

regex = '([a-zA-Z0-9_.+-]+)@[a-zA-Z0-9_.+-]+\.[a-zA-Z0-9_.+-]'


# Função para validar email
def checkEmail(email):
    result = False
    if re.search(regex, email):
        result = True
    return result


# Função para validar Grupo de Usuario
def checkGroup(user, group):
    return user.groups.filter(name=group).exists()


# Enviando Email
def enviandoEmail(assunto, mensagem, emails):
    from_email = settings.EMAIL_HOST_USER
    send_mail(assunto, mensagem, from_email, emails, fail_silently=True)


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
