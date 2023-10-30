# Projeto Integrador II UNIVESP - 2º Semestre 2023

## GEPS - Gerenciador Eletrônico de Professores Substitutos

Essas instruções servem normalmente para serem usados com banco 
de dados MySQL e PostgreSQL. Outros bancos podem demandar outras instruções.

### Instalação

Baixar esse código e colocar ele em uma pasta visível pelo Apache.

### Instalação das bibliotecas necessárias

Use em linha de comando o utilitário `pip` para instalar os seguintes pacotes do Python

+ `django_on_heroku`
+ `dotenv`
+ `django_model_utils`
+ `django_simple_cookie_consent`

#### Preparar visualização de base de dados

Além das configuração abaixo verifique a necessidade de ajustes de segurança no seu servidor

+ MySQL

No arquivo `mysqld.cnf`, procure a sessão `[mysql]` e ajuste `bind-address` para o ip do servidor do GEPS ou uma lista de ips necessários

> + ***OPÇÃO NÃO SEGURA:*** Ajuste `bind-address` para `0.0.0.0`. Qualquer servidor passa a ser acessado. Cuidado!
> + Em caso de mensagem de erro *Public Key Retrieval is not allowed* defina as opções abaixo em seu cliente de SQL
>    + `useSSL` como `false`
>    + `allowPublicKeyRetrieval` com `true`

```
[mysql]
...
...
...
...
bind-address		= 0.0.0.0
mysqlx-bind-address	= 0.0.0.0
```

+ PostgreSQL

Após a instalação do PostgreSQL, entre via shell como usuário `postgres`

> `sudo su - postgres`

Ou no Ubuntu edite como `root` os arquivos abaixo:

+ <version>/main/postgresql.conf:

Modifique a variável `listen_address` para o valor abaixo

```
listen_addresses = '*'			
```

+ <version>/main/pg_hba.conf:

Coloque a linha abaixo no final do arquivo

```
host    all             all             0.0.0.0/32              md5
```

#### Criar Usuário de Banco de dados

+ MySQL

Acessando o banco com um usuário administrativo, (usualmente `root`), use o comando abaixo

> `CREATE USER '<usuario>'@'<ip>' IDENTIFIED BY '<senha>'`

Algumas versões mais novas do MySQL possuem questões sobre a qualidade da senha. 

> + ***OPÇÃO NÃO SEGURA:*** Ao criar o usuário, utilize `*` no IP para autorizar acesso com esse usuário a partir de qualquer lugar. Pode ser interessante mudar a senha para determinados locais.
> + [Documentação sobre os níveis de segurança de senha](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/secure-deployment-password-validation.html)

+ PostgreSQL

Como usuário administrativo, (usualmente `postgres`), use o comando abaixo

> `CREATE USER <usuario> IDENTIFIED BY '<senha>'`

#### Criar Base de Dados

+ MySQL e PostgreSQL

Ainda como usuário administrativo, use o comando abaixo para criar o banco

`CREATE DATABASE <usuario>`

#### Configuração Inicial do Banco

Após criar o usuário e o banco, dê permissão ao banco para aquele usuário usuário. Pela forma como o banco é criado, é necessário permissões completas ao banco para esse usuário (ao menos para a primeira vez), pois o Django criará todas as tabelas, índices e restrições.

+ MySQL

+ `GRANT ALL ON <banco>.* to '<usuario>'@'<ip>'` - coloque o mesmo usuário e IP anteriormente descrito


+ PostgreSQL

`GRANT ALL ON DATABASE <banco> to <usuario>;` - coloque o mesmo usuário e IP anteriormente descrito

Para tudo funcionar bem no PostgreSQL, é necessártio também passar a posse do banco para o usuário do banco

`ALTER DATABASE <abnco> OWNER TO <usuario;`


#### Ajustes de `settings.py`

+ MySQL

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<banco>',
        'HOST': '<ip do servidor>',
        'USER': '<usuario>',
        'PASSWORD': '<senha>',
        'PORT': '<porta>' # padrão 3306
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

+ PostgreSQL

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<banco>',
        'HOST': '<ip do servidor>',
        'USER': '<usuario>',
        'PASSWORD': '<senha>',
        'PORT': '<porta>' # padrão 5432
    }
}
```

#### Montar a Estrutura de Base de dados

#### Outros Ajustes a serem executados
