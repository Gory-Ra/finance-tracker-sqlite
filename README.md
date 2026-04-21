# finance-tracker-sqlite

Um sistema de gerenciamento financeiro em linha de comando (CLI) desenvolvido em Python, utilizando SQLite para persistência de dados.

## 📌 Sobre o projeto

O **finance-tracker-sqlite** é um projeto simples que simula operações básicas de um sistema bancário, permitindo o controle de contas, movimentações financeiras e visualização de dados.

Este projeto foi desenvolvido com fins de **aprendizado e portfólio**, sendo baseado em uma aula do canal **Pythonando**, com adaptações e melhorias para prática pessoal.

## 🚀 Funcionalidades

* Criar contas bancárias
* Listar contas cadastradas
* Desativar contas (com validação de saldo)
* Transferir valores entre contas
* Registrar entradas e saídas de dinheiro
* Consultar histórico de transações por período
* Calcular o total geral das contas
* Gerar gráfico de saldo por conta utilizando matplotlib

## 🛠️ Tecnologias utilizadas

* Python
* SQLite
* SQLModel
* Matplotlib

## 🧠 Conceitos aplicados

* Programação orientada a objetos (POO)
* Estrutura em camadas (separação entre modelo, lógica e interface)
* Manipulação de banco de dados com ORM
* Validações de regras de negócio
* Interface via linha de comando (CLI)

## 📂 Estrutura do projeto

```
.
├── models.py      # Definição das tabelas e conexão com o banco
├── view.py        # Regras de negócio e manipulação dos dados
├── templates.py   # Interface de interação com o usuário (CLI)
└── database.db    # Banco de dados SQLite
```

## ⚙️ Como executar o projeto

1. Clone o repositório:

```
git clone https://github.com/seu-usuario/finance-tracker-sqlite.git
```

2. Acesse a pasta do projeto:

```
cd finance-tracker-sqlite
```

3. Instale as dependências:

```
pip install sqlmodel matplotlib
```

4. Execute o projeto:

```
python templates.py
```

## 📊 Exemplo de uso

O sistema funciona via terminal, apresentando um menu com opções como:

```
[1] Criar conta
[2] Desativar conta
[3] Transferir dinheiro
[4] Movimentar dinheiro
[5] Total contas
[6] Filtrar histórico
[7] Gráfico
```

## 🎯 Objetivo

Este projeto tem como objetivo consolidar conhecimentos em:

* Python
* Banco de dados
* Estruturação de projetos
* Lógica de sistemas financeiros

## 📚 Créditos

Projeto baseado em conteúdo educacional do canal **Pythonando**, utilizado como material de estudo e prática.

---

## 📄 Licença

Este projeto é livre para uso educacional.
