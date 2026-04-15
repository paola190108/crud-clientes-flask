import psycopg2
import os
from flask import Flask, request, jsonify, render_template
from crud.usuarios import (
    criar_tabela, criar_usuario, listar_usuarios,
    buscar_por_id, buscar_por_nome, buscar_por_email,
    atualizar_usuario, deletar_usuario,
)

app = Flask(__name__)

# Tenta criar a tabela ao iniciar a aplicação
try:
    with app.app_context():
        criar_tabela()
except Exception as e:
    print(f"Aguardando banco de dados... Erro: {e}")

def ok(data=None, status=200, msg=None):
    body = {"status": "ok"}
    if msg: body["mensagem"] = msg
    if data is not None: body["data"] = data
    return jsonify(body), status

def erro(mensagem, status=400):
    return jsonify({"status": "erro", "mensagem": mensagem}), status

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/usuarios")
def get_usuarios():
    return ok(listar_usuarios())

@app.get("/usuarios/buscar/nome")
def get_buscar_nome():
    q = request.args.get("q", "").strip()
    if not q: return erro("Informe o nome.")
    return ok(buscar_por_nome(q))

@app.get("/usuarios/buscar/email")
def get_buscar_email():
    q = request.args.get("q", "").strip()
    if not q: return erro("Informe o email.")
    usuario = buscar_por_email(q)
    return ok(usuario) if usuario else erro("Não encontrado.", 404)

@app.get("/usuarios/<int:usuario_id>")
def get_usuario(usuario_id):
    usuario = buscar_por_id(usuario_id)
    return ok(usuario) if usuario else erro("Não encontrado.", 404)

@app.post("/usuarios")
def post_usuario():
    body = request.get_json(silent=True) or {}
    nome, email = body.get("nome", "").strip(), body.get("email", "").strip()
    if not nome or not email: return erro("Nome e Email são obrigatórios.")
    try:
        novo_id = criar_usuario(nome, email, body.get("telefone"), 
                                body.get("cidade"), body.get("empresa"), body.get("cpf_cnpj"))
        return ok({"id": novo_id}, 201, "Criado com sucesso.")
    except psycopg2.IntegrityError:
        return erro("Email ou CPF/CNPJ já cadastrado.", 409)

@app.put("/usuarios/<int:usuario_id>")
def put_usuario(usuario_id):
    body = request.get_json(silent=True) or {}
    try:
        sucesso = atualizar_usuario(usuario_id, nome=body.get("nome"), email=body.get("email"),
                                    telefone=body.get("telefone"), cidade=body.get("cidade"),
                                    empresa=body.get("empresa"), cpf_cnpj=body.get("cpf_cnpj"))
        return ok(msg="Atualizado.") if sucesso else erro("Não encontrado.", 404)
    except psycopg2.IntegrityError:
        return erro("Dados conflitantes com outro usuário.", 409)

@app.delete("/usuarios/<int:usuario_id>")
def delete_usuario(usuario_id):
    return ok(msg="Deletado.") if deletar_usuario(usuario_id) else erro("Não encontrado.", 404)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)