-- ==========================================================
-- Script SQL - Catálogo de Filmes e Séries
-- Etapa 7 - ORM acessando o banco criado
-- Sarah Oliveira Lucas Diógenes
-- ==========================================================
# Catálogo de Filmes e Séries - ORM com SQLAlchemy

Este projeto implementa um sistema de gerenciamento de catálogo de filmes e séries utilizando **Python, SQLAlchemy e PostgreSQL**.

A aplicação demonstra:

- Conexão com banco de dados PostgreSQL
- Mapeamento ORM com SQLAlchemy
- Operações CRUD
- Consultas com relacionamento entre tabelas
- Consultas com agregação e ordenação


# Tecnologias utilizadas

- Python 3
- PostgreSQL
- SQLAlchemy
- Psycopg2
- VS Code
- DBeaver


# Estrutura do Projeto

O projeto possui os seguintes arquivos principais:

- [database.py](database.py) → configuração da conexão com o banco de dados PostgreSQL.
- [`models.py`](models.py) → definição das entidades ORM e os relacionamentos entre as tabelas.
- [`main.py`](main.py) → execução das operações CRUD e consultas
- [text](README.md)
- [text](requeriments.txt)
- [text](<Script do Banco e Dados de teste>) -> script do banco de dados


# Configuração do Banco de Dados

A conexão com o banco é configurada no arquivo (database.py).

```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"

A URL de conexão utilizada pelo SQLAlchemy é:

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

Observação: essas credenciais podem mudar de acordo com a máquina, sendo necessário mudar os valores.

# Como executar o projeto



