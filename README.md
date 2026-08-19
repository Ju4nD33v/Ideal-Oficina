#  Ideal Oficina — Sistema de Gestão para Oficina Mecânica

> Sistema de gestão para oficinas mecânicas desenvolvido em Python, MySQL e FastAPI, com interface web integrada ao backend.

##  Sobre o projeto

O **Ideal Oficina** é uma aplicação criada para organizar e centralizar informações de uma oficina mecânica, permitindo controlar clientes, veículos, mecânicos, peças e ordens de serviço em um único sistema.

O projeto começou como uma aplicação Python executada pelo terminal e evoluiu para uma arquitetura com **API REST + interface web**, mantendo a conexão com o banco de dados MySQL.

A aplicação foi desenvolvida como projeto prático de Engenharia de Software para estudar e aplicar conceitos de:

- Python;
- MySQL;
- SQL;
- APIs REST;
- FastAPI;
- Pydantic;
- HTML, CSS e JavaScript;
- integração entre frontend e backend;
- validação de dados;
- consultas SQL parametrizadas;
- relacionamentos entre tabelas;
- operações CRUD/parciais;
- organização de código por camadas;
- tratamento de erros;
- ambientes virtuais Python;
- gerenciamento de variáveis de ambiente.

---

##  Problema que o projeto resolve

Oficinas podem precisar controlar diversas informações simultaneamente: dados dos clientes, veículos, mecânicos, peças, serviços realizados e ordens de serviço.

Quando essas informações ficam espalhadas em anotações, planilhas ou sistemas separados, torna-se mais difícil acompanhar o histórico dos atendimentos, localizar informações e controlar o andamento das ordens.

O Ideal Oficina busca centralizar essas informações em uma aplicação que permita:

- cadastrar clientes;
- relacionar veículos aos respectivos proprietários;
- cadastrar mecânicos e suas especialidades;
- manter um catálogo de peças;
- registrar serviços e mão de obra;
- criar ordens de serviço;
- acompanhar o status das ordens;
- consultar informações de forma organizada;
- visualizar indicadores da oficina através de um dashboard.

---

##  Funcionalidades

###  Dashboard

O dashboard apresenta indicadores gerais da oficina:

- quantidade de clientes;
- quantidade de veículos;
- quantidade de mecânicos;
- quantidade de peças;
- quantidade de ordens de serviço;
- distribuição das ordens por status;
- ordens de serviço recentes.

Quando o banco está vazio, os indicadores são apresentados como `0` e as áreas de listagem exibem estados vazios amigáveis em vez de tratar a ausência de registros como erro.

---

###  Clientes

Permite:

- listar clientes cadastrados;
- pesquisar clientes por nome ou telefone;
- visualizar ID, nome, telefone e endereço;
- cadastrar novos clientes;
- validar os dados enviados pela API;
- impedir o cadastro com campos obrigatórios vazios.

Endpoint principal:

```text
GET  /api/clientes
POST /api/clientes
GET  /api/clientes/{cliente_id}
```

Exemplo de cadastro:

```json
{
  "nome": "João da Silva",
  "telefone": "16999999999",
  "endereco": "Rua das Flores, 100"
}
```

Também existe a rota legada:

```text
GET /clientes/
```

mantida para compatibilidade com a primeira versão da API.

---

###  Veículos

Permite:

- listar veículos;
- visualizar modelo, cor, ano e placa;
- visualizar o problema apresentado;
- identificar o cliente proprietário;
- cadastrar veículos relacionados a um cliente existente.

Endpoint:

```text
GET  /api/veiculos
POST /api/veiculos
```

Exemplo:

```json
{
  "modelo": "Honda Civic",
  "cor": "Prata",
  "ano": "2022",
  "problema": "Falha no sistema de freios",
  "dono_veiculo": 1,
  "placa": "ABC1D23"
}
```

A API verifica se o cliente informado existe antes de cadastrar o veículo.

---

###  Mecânicos

Permite:

- listar mecânicos;
- visualizar especialidade;
- visualizar endereço;
- visualizar código do mecânico;
- cadastrar mecânicos;
- gerar automaticamente um código numérico para o mecânico.

Endpoint:

```text
GET  /api/mecanicos
POST /api/mecanicos
```

Exemplo:

```json
{
  "nome": "Carlos Oliveira",
  "endereco": "Rua A, 200",
  "especialidade": "Freios e suspensão"
}
```

Após o cadastro, a API retorna o código gerado para o mecânico.

---

###  Peças

Permite:

- listar peças cadastradas;
- visualizar nome;
- visualizar valor;
- visualizar tempo de garantia;
- visualizar descrição;
- cadastrar novas peças.

Endpoint:

```text
GET  /api/pecas
POST /api/pecas
```

Exemplo:

```json
{
  "nome": "Pastilha de freio",
  "valor": 180.50,
  "garantia": "12 meses",
  "descricao": "Pastilha dianteira"
}
```

---

###  Ordens de serviço

Permite:

- listar ordens de serviço;
- visualizar veículo associado;
- visualizar placa;
- visualizar mecânico responsável;
- visualizar data de emissão;
- visualizar data de conclusão;
- visualizar status;
- visualizar valor total;
- criar novas ordens de serviço;
- atualizar o status de uma OS.

Endpoints:

```text
GET   /api/ordens-servico
POST  /api/ordens-servico
PATCH /api/ordens-servico/{id}/status
```

A criação de uma ordem verifica a existência de:

- veículo;
- mecânico;
- peça.

A mão de obra é registrada na tabela `mao_de_obra`, relacionada a um serviço, e o serviço é relacionado à ordem de serviço.

O valor total da OS é calculado pela aplicação como:

```text
valor total = valor da mão de obra + valor da peça selecionada
```

Exemplo de criação:

```json
{
  "veiculo_id": 1,
  "mecanico_id": 1,
  "peca_id": 1,
  "status": "Em análise",
  "data_conclusao": "2026-08-25",
  "mao_de_obra": "Substituição das pastilhas de freio",
  "valor_mao_de_obra": 150.00
}
```

Status disponíveis na interface incluem:

- `Em análise`;
- `Em andamento`;
- `Aguardando peça`;
- `Concluída`;
- `Cancelada`.

O status também pode ser atualizado posteriormente pela interface.

---

##  Interface web

A interface é desenvolvida com:

- HTML5;
- CSS3;
- JavaScript puro;
- FastAPI para servir os arquivos estáticos.

Não é necessário Node.js, npm, React ou Vite para executar a versão atual da interface.

### Telas disponíveis

- Dashboard;
- Clientes;
- Veículos;
- Ordens de serviço;
- Mecânicos;
- Peças.

A interface possui:

- menu lateral;
- dashboard com indicadores;
- tabelas para visualização dos dados;
- formulários em janelas modais;
- mensagens de sucesso e erro;
- botão de atualização;
- relógio no cabeçalho;
- estados vazios para tabelas sem registros;
- tratamento visual para erros da API;
- atualização das páginas após operações de cadastro;
- layout responsivo.

---

##  Arquitetura

A aplicação segue o fluxo:

```text
┌─────────────────────────────────────────┐
│              INTERFACE WEB              │
│          HTML + CSS + JavaScript        │
│                                         │
│ Dashboard | Clientes | Veículos         │
│ OS | Mecânicos | Peças                  │
└────────────────────┬────────────────────┘
                     │
                     │ HTTP / JSON
                     ▼
┌─────────────────────────────────────────┐
│                 FASTAPI                 │
│                                         │
│ /api/dashboard                          │
│ /api/clientes                           │
│ /api/veiculos                           │
│ /api/mecanicos                          │
│ /api/pecas                              │
│ /api/ordens-servico                     │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│                CAMADA DB                │
│       conexão + consultas SQL            │
└────────────────────┬────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────┐
│                  MYSQL                  │
│                                         │
│ cliente                                 │
│ veiculo_cliente                          │
│ equipe_mecanico                          │
│ tabela_peças                             │
│ mao_de_obra                              │
│ serviços                                 │
│ serviços_os                              │
│ peças_na_os                              │
│ ordem_de_serviço                         │
└─────────────────────────────────────────┘
```

O projeto também mantém a aplicação original de terminal em `main/main.py`.

---

##  Banco de dados

O banco utilizado pelo projeto é o **MySQL**.

Banco padrão:

```text
oficina_mecanica
```

As tabelas utilizadas pela versão atual são:

```text
cliente
equipe_mecanico
veiculo_cliente
ordem_de_serviço
tabela_peças
mao_de_obra
serviços
serviços_os
peças_na_os
```

### Relacionamentos principais

```text
cliente
   │
   └── veiculo_cliente
          │
          └── ordem_de_serviço
                 │
                 ├── equipe_mecanico
                 │
                 ├── serviços_os ── serviços ── mao_de_obra
                 │
                 └── peças_na_os ── tabela_peças
```

O arquivo `database/banco.sql` contém a estrutura de criação do banco e das tabelas.

> **Importante:** se você já possui o banco `oficina_mecanica` criado e com dados, não execute o script indiscriminadamente por cima de uma base de produção. O script utiliza `CREATE ... IF NOT EXISTS`, mas alterações de estrutura existentes não são automaticamente migradas.

---

#  Instalação

## 1. Pré-requisitos

Instale:

- Python 3.9 ou superior;
- MySQL Server;
- Git, caso queira versionar o projeto;
- VS Code ou outro editor de código, opcionalmente.

O projeto atual foi desenvolvido e testado em ambiente Python com `venv`.

---

## 2. Clonar o projeto

Caso esteja usando GitHub:

```bash
git clone URL_DO_SEU_REPOSITORIO
cd Ideal-Oficina
```

Ou simplesmente abra a pasta do projeto no VS Code.

---

## 3. Criar o ambiente virtual

Na raiz do projeto:

### Windows PowerShell

```powershell
python -m venv venv
```

Ative o ambiente:

```powershell
.\venv\Scripts\Activate.ps1
```

O terminal deverá mostrar algo semelhante a:

```text
(venv) PS C:\Users\Usuario\Desktop\Ideal-Oficina>
```

### Windows CMD

```cmd
venv\Scripts\activate
```

---

## 4. Instalar as dependências

Com o ambiente virtual ativo:

```bash
python -m pip install -r requirements.txt
```

Dependências principais:

```text
fastapi
mysql-connector-python
pydantic
python-dotenv
uvicorn
```

---

#  Configuração do banco

## 5. Criar o arquivo `.env`

O projeto não deve armazenar a senha do MySQL no código-fonte.

Existe um modelo em:

```text
senhas/.env.example
```

Crie uma cópia chamada:

```text
senhas/.env
```

Exemplo:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=sua_senha
DB_DATABASE=oficina_mecanica
```

Substitua `sua_senha` pela senha do seu MySQL.

### Segurança

O arquivo `.env` está incluído no `.gitignore` e **não deve ser enviado ao GitHub**.

Não coloque senhas, tokens ou credenciais diretamente no código Python.

---

#  Preparar o MySQL

Se você ainda não possui o banco, abra o MySQL Workbench ou outro cliente MySQL e execute:

```text
database/banco.sql
```

Isso cria o banco:

```text
oficina_mecanica
```

e as tabelas necessárias.

Depois confirme:

```sql
USE oficina_mecanica;
SHOW TABLES;
```

Você deverá encontrar as tabelas utilizadas pelo sistema.

---

#  Executar a API e a interface

Com o `venv` ativo e o `.env` configurado:

```powershell
python -m uvicorn api.main:app --reload
```

Quando funcionar, aparecerá algo semelhante a:

```text
Uvicorn running on http://127.0.0.1:8000
```

Abra no navegador:

```text
http://127.0.0.1:8000
```

A interface web será carregada pelo próprio FastAPI.

---

##  Executar pelo arquivo `.bat`

No Windows, o projeto também possui:

```text
start_api.bat
```

Ele automatiza a ativação do ambiente virtual e a inicialização do Uvicorn.

Basta executar:

```text
start_api.bat
```

O ambiente virtual precisa existir previamente.

---

#  Documentação da API

O FastAPI gera automaticamente a documentação interativa.

## Swagger UI

Abra:

```text
http://127.0.0.1:8000/docs
```

Nessa página é possível visualizar os endpoints, seus métodos, parâmetros e schemas e testar requisições diretamente no navegador.

## Health Check

Para verificar se a API está online:

```text
GET http://127.0.0.1:8000/api/health
```

Resposta esperada:

```json
{
  "status": "online",
  "application": "Ideal Oficina"
}
```

---

#  Endpoints da API

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/health` | Verifica se a API está online |
| GET | `/api/dashboard` | Retorna indicadores, status e OS recentes |
| GET | `/api/clientes` | Lista clientes |
| GET | `/api/clientes/{id}` | Consulta um cliente específico |
| POST | `/api/clientes` | Cadastra cliente |
| GET | `/api/veiculos` | Lista veículos |
| POST | `/api/veiculos` | Cadastra veículo |
| GET | `/api/mecanicos` | Lista mecânicos |
| POST | `/api/mecanicos` | Cadastra mecânico |
| GET | `/api/pecas` | Lista peças |
| POST | `/api/pecas` | Cadastra peça |
| GET | `/api/ordens-servico` | Lista ordens de serviço |
| POST | `/api/ordens-servico` | Cria ordem de serviço |
| PATCH | `/api/ordens-servico/{id}/status` | Atualiza status da OS |
| GET | `/clientes/` | Rota legada para compatibilidade |

---

#  Exemplos de requisições

## Criar cliente

```http
POST /api/clientes
Content-Type: application/json
```

```json
{
  "nome": "João Silva",
  "telefone": "16999999999",
  "endereco": "Rua das Flores, 100"
}
```

---

## Criar veículo

O cliente precisa existir antes.

```http
POST /api/veiculos
Content-Type: application/json
```

```json
{
  "modelo": "Honda Civic",
  "cor": "Prata",
  "ano": "2022",
  "problema": "Problema no sistema de freios",
  "dono_veiculo": 1,
  "placa": "ABC1D23"
}
```

---

## Criar mecânico

```http
POST /api/mecanicos
Content-Type: application/json
```

```json
{
  "nome": "Carlos Oliveira",
  "endereco": "Rua A, 200",
  "especialidade": "Freios e suspensão"
}
```

---

## Criar peça

```http
POST /api/pecas
Content-Type: application/json
```

```json
{
  "nome": "Pastilha de freio",
  "valor": 180.50,
  "garantia": "12 meses",
  "descricao": "Pastilha dianteira"
}
```

---

## Criar ordem de serviço

Para criar uma OS, é necessário possuir pelo menos:

- um veículo;
- um mecânico;
- uma peça.

```http
POST /api/ordens-servico
Content-Type: application/json
```

```json
{
  "veiculo_id": 1,
  "mecanico_id": 1,
  "peca_id": 1,
  "status": "Em análise",
  "data_conclusao": "2026-08-25",
  "mao_de_obra": "Substituição das pastilhas de freio",
  "valor_mao_de_obra": 150.00
}
```

---

## Atualizar status da OS

```http
PATCH /api/ordens-servico/1/status
Content-Type: application/json
```

```json
{
  "status": "Concluída"
}
```

---

#  Estrutura do projeto

```text
Ideal-Oficina/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── clientes.py
│       ├── dashboard.py
│       ├── mecanicos.py
│       ├── ordens.py
│       ├── pecas.py
│       └── veiculos.py
│
├── database/
│   ├── __init__.py
│   ├── banco.sql
│   └── conexao.py
│
├── main/
│   ├── __init__.py
│   └── main.py
│
├── services/
│   ├── __init__.py
│   ├── cliente.py
│   ├── mecanico.py
│   ├── ordem_servico.py
│   ├── pecas.py
│   └── veiculo.py
│
├── senhas/
│   └── .env.example
│
├── tests/
│   └── .gitkeep
│
├── web/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── .gitignore
├── requirements.txt
├── start_api.bat
└── README.md
```

### `api/`

Contém a API FastAPI, os schemas de validação, acesso ao banco e as rotas HTTP.

### `api/routes/`

Organiza os endpoints por recurso:

- clientes;
- dashboard;
- mecânicos;
- ordens de serviço;
- peças;
- veículos.

### `api/schemas.py`

Define os modelos de entrada utilizados pelo Pydantic para validar os dados recebidos pela API.

### `api/db.py`

Centraliza funções para:

- consultas que retornam várias linhas;
- consultas que retornam uma linha;
- comandos de escrita com commit e rollback.

### `database/`

Contém a conexão com o MySQL e o script SQL da estrutura do banco.

### `services/`

Mantém a lógica da aplicação original desenvolvida para o terminal.

### `main/`

Contém o ponto de entrada da aplicação de terminal original.

### `web/`

Contém a interface web:

- `index.html`: estrutura da aplicação;
- `styles.css`: estilos visuais;
- `app.js`: comunicação com a API e comportamento da interface.

### `tests/`

Estrutura reservada para testes automatizados futuros.

### `senhas/.env`

Contém as credenciais locais do banco. Não deve ser versionado.

---

#  Fluxo de funcionamento

Quando o usuário acessa a aplicação:

```text
Navegador
   ↓
GET /
   ↓
FastAPI
   ↓
web/index.html
```

Quando a interface precisa dos dados:

```text
JavaScript
   ↓
GET /api/clientes
   ↓
FastAPI
   ↓
api/routes/clientes.py
   ↓
api/db.py
   ↓
database/conexao.py
   ↓
MySQL
   ↓
JSON
   ↓
JavaScript
   ↓
Tabela na interface
```

Para um cadastro:

```text
Formulário
   ↓
JavaScript
   ↓
POST /api/clientes
   ↓
Pydantic
   ↓
Validação
   ↓
SQL parametrizado
   ↓
MySQL
   ↓
Commit
   ↓
Resposta JSON
   ↓
Interface atualizada
```

---

#  Segurança e boas práticas implementadas

O projeto utiliza algumas práticas importantes:

### Queries parametrizadas

Os valores recebidos pela aplicação são enviados como parâmetros das consultas SQL, em vez de serem concatenados diretamente nas strings SQL.

Exemplo conceitual:

```python
cursor.execute(
    "SELECT id FROM cliente WHERE id = %s",
    (cliente_id,)
)
```

Isso reduz o risco de SQL Injection em comparação com a montagem direta de SQL utilizando valores fornecidos pelo usuário.

### Variáveis de ambiente

As credenciais do MySQL são carregadas através do `.env`.

### `.gitignore`

O projeto ignora:

```text
senhas/.env
venv/
.venv/
__pycache__/
*.pyc
.vscode/
.idea/
node_modules/
```

### Validação com Pydantic

A API valida tamanho e tipo de diversos campos antes de executar as operações no banco.

### Rollback em operações de escrita

As operações de escrita possuem tratamento para realizar rollback em caso de exceção, evitando manter uma transação parcialmente concluída.

> A aplicação ainda não possui autenticação, autorização, gerenciamento de usuários, JWT ou controle de permissões. Essas funcionalidades estão planejadas para evoluções futuras.

---

#  Banco vazio

A aplicação foi preparada para funcionar mesmo quando as tabelas ainda não possuem registros.

Exemplos:

```text
Clientes: 0
Veículos: 0
Mecânicos: 0
Peças: 0
Ordens: 0
```

Nas páginas de listagem, o sistema apresenta mensagens como:

```text
Nenhum cliente cadastrado
Nenhum veículo cadastrado
Nenhum mecânico cadastrado
Nenhuma peça cadastrada
Nenhuma ordem de serviço cadastrada
```

A ausência de registros é tratada como um estado válido do sistema.

Para criar uma ordem de serviço, entretanto, é necessário primeiro cadastrar os dados relacionados exigidos pela operação: veículo, mecânico e peça.

---

#  Desenvolvimento e testes manuais

Para testar a aplicação durante o desenvolvimento:

1. Ative o `venv`.
2. Confirme que o MySQL está em execução.
3. Confirme o `.env`.
4. Execute o Uvicorn.
5. Abra `/docs`.
6. Teste os endpoints individualmente.
7. Depois teste os mesmos fluxos pela interface web.

Fluxo recomendado para testar a aplicação do zero:

```text
1. Cadastrar cliente
        ↓
2. Cadastrar veículo
        ↓
3. Cadastrar mecânico
        ↓
4. Cadastrar peça
        ↓
5. Criar ordem de serviço
        ↓
6. Consultar a OS
        ↓
7. Atualizar status
        ↓
8. Conferir indicadores no Dashboard
```

---

#  Testes automatizados

A pasta `tests/` está preparada para receber testes automatizados, mas a versão atual ainda não possui uma suíte de testes implementada.

Uma evolução recomendada é utilizar `pytest` e testar:

- schemas;
- endpoints;
- validações;
- consultas;
- criação de clientes;
- criação de veículos;
- criação de mecânicos;
- criação de peças;
- criação de ordens de serviço;
- atualização de status;
- respostas quando o banco está vazio;
- tratamento de erros.

---

#  Solução de problemas

## `ModuleNotFoundError`

Confirme se o ambiente virtual está ativo:

```powershell
.\venv\Scripts\Activate.ps1
```

Depois instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

---

## Erro de conexão com MySQL

Confirme:

```env
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=sua_senha
DB_DATABASE=oficina_mecanica
```

Também confirme se o serviço do MySQL está executando.

Teste a conexão pela própria aplicação ou através do MySQL Workbench.

---

## `Table doesn't exist`

Confirme se o banco selecionado no `.env` é o correto:

```env
DB_DATABASE=oficina_mecanica
```

Depois execute:

```sql
USE oficina_mecanica;
SHOW TABLES;
```

Os nomes das tabelas precisam corresponder à estrutura utilizada pela aplicação, incluindo os nomes que possuem caracteres acentuados.

---

## Porta 8000 ocupada

Execute o Uvicorn em outra porta:

```powershell
python -m uvicorn api.main:app --reload --port 8001
```

Depois abra:

```text
http://127.0.0.1:8001
```

---

#  Possíveis evoluções

O projeto pode evoluir para uma solução mais completa com:

- autenticação de usuários;
- login para administradores, clientes e mecânicos;
- JWT e controle de sessão;
- controle de permissões;
- histórico de serviços por veículo;
- múltiplas peças em uma mesma OS;
- controle de estoque;
- quantidade de peças utilizadas;
- fornecedores;
- orçamento antes da aprovação da OS;
- emissão de PDF da ordem de serviço;
- envio de notificações;
- filtros e paginação;
- relatórios financeiros;
- testes automatizados;
- Docker;
- CI/CD;
- deploy em nuvem;
- banco de dados gerenciado;
- migrações de banco com Alembic;
- logs estruturados;
- tratamento centralizado de exceções;
- documentação mais detalhada da API;
- migração futura do frontend para React + TypeScript.

---

#  Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal do backend e aplicação original |
| FastAPI | Criação da API REST e servidor web |
| Pydantic | Validação dos dados recebidos pela API |
| MySQL | Banco de dados relacional |
| mysql-connector-python | Conexão Python ↔ MySQL |
| python-dotenv | Leitura das variáveis do `.env` |
| Uvicorn | Servidor ASGI para executar o FastAPI |
| HTML5 | Estrutura da interface |
| CSS3 | Estilização da interface |
| JavaScript | Comunicação com a API e lógica do frontend |
| Git/GitHub | Versionamento do projeto |

---

#  Licença

Este projeto é um projeto pessoal de estudos e portfólio.

Caso seja publicado no GitHub, recomenda-se adicionar uma licença explícita ao repositório de acordo com a intenção de uso e distribuição do projeto.

---

#  Sobre o desenvolvimento

O Ideal Oficina é um projeto desenvolvido para praticar o desenvolvimento de uma aplicação completa, passando pela modelagem do banco de dados, implementação das regras em Python, criação de uma API REST e integração com uma interface web.

O projeto também representa a evolução de uma aplicação inicialmente executada pelo terminal para uma arquitetura na qual o frontend se comunica com o backend através de HTTP e JSON.

**Autor:** Juan Pedro
