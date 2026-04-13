"""
app.py — API REST com Flask + SQLite
Execute: python3 app.py
Acesse:  http://localhost:5000
"""

import sqlite3
from flask import Flask, request, jsonify, render_template
from crud import (
    criar_tabela,
    criar_usuario,
    listar_usuarios,
    buscar_por_id,
    buscar_por_nome,
    buscar_por_email,
    atualizar_usuario,
    deletar_usuario,
)

app = Flask(__name__)

with app.app_context():
    criar_tabela()


def resposta_sucesso(data=None, status=200, mensagem=None):
    body = {"status": "sucesso"}
    if mensagem:
        body["mensagem"] = mensagem

def resposta_erro(mensagem, status=400):
    return jsonify({"status": "resposta_erro", "mensagem": mensagem}), status


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/clientes")
def get_cliente():
    return resposta_sucesso(listar_usuarios())


@app.get("/clientes/buscar/nome")
def get_buscar_nome():
    q = request.args.get("q", "").strip()
    if not q: 
        return resposta_erro("Informe o parâmetro ?q=nome")
    return resposta_sucesso(buscar_por_nome(q))


@app.get("/clientes/buscar/email")
def get_buscar_email():
    email_busca = request.args.get("q", "").strip()
    if not email_busca:
        return resposta_erro("Informe o parâmetro ?q=email")
    cliente = buscar_por_email(email_busca)
    if not cliente:
        return resposta_erro("Cliente não encontrado.", 404)
    return resposta_sucesso(cliente)

@app.get("/clientes/<int:cliente_id>")
def get_cliente(cliente_id):
    cliente = buscar_por_id(cliente_id)
    if not cliente: 
        return resposta_erro("Cliente não encontrado.", 404)
    return resposta_sucesso(cliente)


@app.post("/clientes")
def post_cliente():
    body = request.get_json(silent=True)
    if not body: 
        return resposta_erro("Body JSON obrigatório.")

    nome     = body.get("nome",     "").strip()
    email    = body.get("email",    "").strip()
    telefone = body.get("telefone")
    cidade   = body.get("cidade")
    empresa  = body.get("empresa")
    cpf_cnpj = body.get("cpf_cnpj")

    if not nome: 
        return resposta_erro("Campo 'nome' é obrigatório.")
    if not email: 
        return resposta_erro("Campo 'email' é obrigatório.")

    try:
        novo_id = criar_usuario(nome, email, telefone, cidade, empresa, cpf_cnpj)
        return resposta_sucesso({"id": novo_id}, status=201, msg="Cliente criado.")
    except sqlite3.Integrityresposta_error:
        return resposta_erro("E-mail ou CPF/CNPJ já cadastrado.", 409)


@app.put("/clientes/<int:cliente_id>")
def put_cliente(cliente_id):
    body = request.get_json(silent=True)
    if not body: 
        return resposta_erro("Body JSON obrigatório.")

    try:
        atualizado = atualizar_usuario(
            cliente_id,
            nome     = body.get("nome"),
            email    = body.get("email"),
            telefone = body.get("telefone"),
            cidade   = body.get("cidade"),
            empresa  = body.get("empresa"),
            cpf_cnpj = body.get("cpf_cnpj"),
        )
    except sqlite3.Integrityresposta_error:
        return resposta_erro("E-mail ou CPF/CNPJ já pertence a outro cliente.", 409)

    if not atualizado: return resposta_erro("Cliente não encontrado.", 404)
    return resposta_sucesso(msg="Cliente atualizado.")


@app.delete("/clientes/<int:cliente_id>")
def delete_usuario(cliente_id):
    deletado = deletar_usuario(cliente_id)
    if not deletado: return resposta_erro("Cliente não encontrado.", 404)
    return resposta_sucesso(msg="Cliente deletado.")


if __name__ == "__main__":
    app.run(debug=True, port=5000)