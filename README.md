# Projeto Integrador UniVESP 1º Semestre 2024

## GEPS

Essas instruções seguem normalmente para serem usados com banco de dados MySQL, MariaDN e PostgreSQL. Outros bancos podem demandar outras instruções

### Instalação

Baixar esse código e colocar ele em uma pasta visível pelo Apache 

### Instalação das bibliotecas necessárias

Use em linha de comando o utilitário `pip` para instalar os seguintes pacotes do Python

> `python3 -m pip install -r requirements.txt`

Além das bibliotecas para o banco de dados desejado (caso não esteja instalado):

+ MySQL/MariaDB: `pip3 install mysql python-mysql`
+ PostegreSQL: `pip3 install mysql pyscopg2`

> ***ATENÇÃO:*** Como esse projeto é baseado no Framework Django, ele é compatível com qualquer banco de dados suportado pelo mesmo, e as funcionalidades não serão diferentes. ***Entretanto*** não será nossa responsabilidade a configuração do banco de dados para esses bancos. O projeto foi focado no uso de MySQL/MariaDB e PostgreSQL, e não foi pensado no uso com outros bancos de dados.

### Configuração do Banco de dados

#### Preparar visualização de base de dados

Além das configuração abaixo verifique a necessidade de ajustes de segurança no seu servidor

+ MySQL/MariaDB

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

No MariaDB não se faz necessária nenhuma modificação

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

+ MySQL/MariaDB

Acessando o banco com um usuário administrativo, (usualmente `root`), use o comando abaixo

> `CREATE USER '<usuario>'@'<ip>' IDENTIFIED BY '<senha>'`

Algumas versões mais novas do MySQL possuem questões sobre a qualidade da senha. 

Caso não seja possível utilizar em um comando só use:

```
CREATE USER '<usuario>'@'<ip>';
ALTER USER '<usuario>'@'<ip>' PASSWORD '<senha>'`;
```

> + ***OPÇÃO NÃO SEGURA:*** Ao criar o usuário, utilize `%` no IP para autorizar acesso com esse usuário a partir de qualquer lugar. Pode ser interessante mudar a senha para determinados locais.
> + [Documentação sobre os níveis de segurança de senha](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/secure-deployment-password-validation.html)

+ PostgreSQL

Como usuário administrativo, (usualmente `postgres`), use o comando abaixo

> `CREATE USER <usuario> IDENTIFIED BY '<senha>'`;

#### Criar Base de Dados

+ MySQL/MariaDB e PostgreSQL

Ainda como usuário administrativo, use o comando abaixo para criar o banco

`CREATE DATABASE <usuario>`;

#### Configuração Inicial do Banco

Após criar o usuário e o banco, dê permissão ao banco para aquele usuário usuário. Pela forma como o banco é criado, é necessário permissões completas ao banco para esse usuário (ao menos para a primeira vez), pois o Django criará todas as tabelas, índices e restrições.

+ MySQL/MariaDB

+ `GRANT ALL ON <banco>.* to '<usuario>'@'<ip>'` - coloque o mesmo usuário e IP anteriormente descrito


+ PostgreSQL

`GRANT ALL ON DATABASE <banco> to <usuario>;` - coloque o mesmo usuário e IP anteriormente descrito

Para tudo funcionar bem no PostgreSQL, é necessártio também passar a posse do banco para o usuário do banco

`ALTER DATABASE <abnco> OWNER TO <usuario>;`

### Ajustes de `settings.py`

Em `projetointegrador/settings.py`, modifique a sessão DATABASES corretamente de acordo com o banco. Lembre-se de instalar (via `pip` ou de acordo com o sistema operacional utilizado) os pacotes adequados para o banco em questão

+ MySQL/MariaDB: `pip3 install mysql python-mysql`
+ PostegreSQL: `pip3 install mysql pyscopg2`

+ MySQL/MariaDB

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<banco>',
        'HOST': '<ip do servidor>',
        'USER': '<usuario>',
        'PASSWORD': '<senha>',
        'PORT': '<porta>', # padrão 3306
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

### Outros Ajustes a serem executados

Antes de aplicar as migrações para a criação básica do banco de dados, serão necessários ajustes em arquivos para a carga inicial de dados.

Use um dos arquivos exemplo, `migrations/0016_carrega_cidades_sa.py` ou `migrations/0017_carrega_cidades_cotia.py` conforme as orientações abaixo, copiando o arquivo desejado com o nome do destino no formato `migrations/XXXX_carrega_bairros_<nome_cidade>.py` onde:

> + `XXXX` é um número sequencial dentro dos arquivos de migração na pasta `migrations/`. Esse número deve ser, no nome do seu arquivo, igual ao próximo número na sequência.
> + `<nome_cidade>` é o nome de sua cidade, sem acentos e com espaços substituídos por *underscores* (`\_`)

+ `migrations/0016_carrega_bairros_sa.py`:

Na linha 13 do código da nova versão:

```
    cidade_id=cidade_model.objects.get(nome = "Santo André", estado__sigla='SP')
```

 mudar:

+ `nome` para o nome da sua cidade;
+ `estado__sigla` para a sigla do estado da sua cidade;

Nas linhas a partir da linha 15:

```
    bairros = ['Acampamento Anchieta', 'Araçaúva', 'Bangu', 'Campestre', 'Campo Grande', 'Casa Branca',

...

<...bairros ...>
<...bairros ...>
<...bairros ...>

...

               'Vila Suíça', 'Vila Tibiriçá', 'Vila Valparaíso', 'Vila Vitória', 'Waisberg']
````

Substitua a lista de bairros incluída pela lista da cidade desejada

Caso sejam múltiplas cidades, copie o código das linhas 15 a 37 e em cada bloco repita o procedimento anterior para a cidade específica desejada

> ***OPCIONAL:*** Caso desejado, pode ser interessante corrigir também na linha 46:
>
> `cidade_id=cidade_model.objects.get(nome = "Cotia", estado__sigla='SP')`
> 
> mudar:
> 
> + `nome` para o nome da sua cidade;
> + `estado__sigla` para a sigla do estado da sua cidade;
>
> Isso ajudará caso seja necessário desfazer mudanças na Migração evitando problemas futuros

+ `migrations/0017_carrega_bairros_cotia.py`:

Inicialmente, será necessário um arquivo em formato texto puro (`.txt`) com a lista dos bairros de sua cidade, um bairro por linha. Esse arquivo deve ser colocado no diretório/pasta `source_data` abaixo de `migrations`

Na linha 14:

`cidade_id=cidade_model.objects.get(nome = "Cotia", estado__sigla='SP')`

 mudar:

+ `nome` para o nome da sua cidade;
+ `estado__sigla` para a sigla do estado da sua cidade;


Na linha 18:

`bairros=open(this_dir + '/bairros_cotia.txt')`

substitua `/bairros_cotia.txt` pelo nome do arquivo criado anteriormente

> ***OPCIONAL:*** Caso desejado, pode ser interessante corrigir também na linha 26:
>
> `cidade_id=cidade_model.objects.get(nome = "Cotia", estado__sigla='SP')`
> 
> mudar:
> 
> + `nome` para o nome da sua cidade;
> + `estado__sigla` para a sigla do estado da sua cidade;
>
> Isso ajudará caso seja necessário desfazer mudanças na Migração evitando problemas futuros

+ Para ambos os casos

Na linha 52 (`carrega_bairro_sa.py`) ou 33 (`carrega_bairro_cotia.py`):

```
    dependencies = [
        ('geps', '0015_alter_regiaometropolitana_regiaometropolitana_and_more'),
    ]
```

Substituir `0015_alter_regiaometropolitana_regiaometropolitana_and_more` para o nome do último arquivo da pasta `migrations` antes do seu.

### Criar a Estrutura de Base de dados

Após todos os ajustes terem sido realizados em `projetointegrador/settings.py`, `migrations/0010_carrega_cidades.py` e `migrations/0011_carrega_bairros.py`, aplique as migrações para que a estrutura do banco seja criada e os dados iniciais carregados de maneira adequada

+ `python3 manage.py migrate`

### Inicializando o GEPS

Nesse momento, você já terá a base do GEPS configurada e o sistema poderá ser inicializado pelo Apache ou por meio de 

+ `python3 manage.py runserver 0.0.0.0:80`

Esse último comando pode demandar permissão de administrador e a janela onde o mesmo for executado não pode ser fechada


