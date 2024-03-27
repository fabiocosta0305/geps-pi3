import requests

data = {"username": "geps", "password": "Univesp@"}
response = requests.post('http://127.0.0.1:8000/login/', data=data)
if response.status_code == 202:
    print('Requisição bem-sucedida')
    if(response.json() == True):
        print('Instituicao')
    else:
        print('Docente')
else:
    print('Requisição falhou')
    print(response.status_code)
