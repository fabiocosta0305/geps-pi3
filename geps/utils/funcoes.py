import re
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
