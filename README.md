# Um sistema CRUD simples e eficiente para gerenciamento de cadastro de clientes.
### Deploy(a versão online está hospedada no **render** com banco de dados **PostgreSQL** via **Neon.tech**):
https://crud-clientes-flask.onrender.com
### Descrição:
Este é um sistema CRUD (Create, Read, Update, Delete) desenvolvido com o objetivo de gerenciar registros de forma simples e eficiente. A aplicação permite cadastrar, visualizar, editar e excluir dados, utilizando uma interface web integrada a um banco de dados local.
O projeto foi desenvolvido como parte do meu aprendizado em desenvolvimento web back-end, com foco em boas práticas e organização de código.
### Tecnologias usadas:
* **Linguagem:** Python
* **Framework Web:** Flask
* **Bancos de Dados:** PostgreSQL (Produção) e SQLite (Local)
* **Frontend:** HTML5, CSS3 e JavaScript (Fetch API)
* **Drivers & Servidores:** Psycopg2, Gunicorn
* **Cloud & Deploy:** Render, Neon.tech, Git & GitHub
### Funcionalidade:
- Cadastro de novos registros
- Listagem de dados
- Edição de informações existentes
- Exclusão de registros
### Aprendizados
Neste projeto, desenvolvi uma aplicação Full Stack integrando **Python (Flask)** com bancos de dados **SQLite** e **PostgreSQL**, dominando a criação de uma arquitetura híbrida que se adapta automaticamente ao ambiente de execução. Aprendi a gerenciar variáveis de ambiente, manipular sintaxes SQL distintas para persistência de dados e utilizar **JavaScript (Fetch API)** para conectar o frontend ao backend. O projeto cobriu todo o ciclo de vida do software: desde o desenvolvimento e controle de versão com **Git** até o deploy automatizado em plataformas de nuvem como **Render** e **Neon.tech**.
### Como executar:
**Clone o repositório:**
    ```bash
    git clone https://github.com/paola190108/crud-clientes-flask
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    python app.py
    ```
    O servidor estará disponível em `http://127.0.0.1:5000`.
