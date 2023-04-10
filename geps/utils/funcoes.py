import re
from django.conf import settings
from django.core.mail import send_mail

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


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
