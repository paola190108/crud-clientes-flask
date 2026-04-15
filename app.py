import sqlite3
from flask import Flask, request, jsonify, render_template
from crud import (
    criar_tabela, criar_usuario, listar_usuarios,
    buscar_por_id, buscar_por_nome, buscar_por_email,
    atualizar_usuario, deletar_usuario,
)

app = Flask(__name__)

with app.app_context():
    criar_tabela()

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
    if not q: return erro("Informe o parâmetro ?q=nome")
    return ok(buscar_por_nome(q))

@app.get("/usuarios/buscar/email")
def get_buscar_email():
    q = request.args.get("q", "").strip()
    if not q: return erro("Informe o parâmetro ?q=email")
    usuario = buscar_por_email(q)
    if not usuario: return erro("Cliente não encontrado.", 404)
    return ok(usuario)

@app.get("/usuarios/<int:usuario_id>")
def get_usuario(usuario_id):
    usuario = buscar_por_id(usuario_id)
    if not usuario: return erro("Cliente não encontrado.", 404)
    return ok(usuario)

@app.post("/usuarios")
def post_usuario():
    body = request.get_json(silent=True)
    if not body: return erro("Body JSON obrigatório.")
    nome     = body.get("nome", "").strip()
    email    = body.get("email", "").strip()
    if not nome:  return erro("Campo 'nome' é obrigatório.")
    if not email: return erro("Campo 'email' é obrigatório.")
    try:
        novo_id = criar_usuario(nome, email,
            body.get("telefone"), body.get("cidade"),
            body.get("empresa"),  body.get("cpf_cnpj"))
        return ok({"id": novo_id}, status=201, msg="Cliente criado.")
    except sqlite3.IntegrityError:
        return erro("E-mail ou CPF/CNPJ já cadastrado.", 409)

@app.put("/usuarios/<int:usuario_id>")
def put_usuario(usuario_id):
    body = request.get_json(silent=True)
    if not body: return erro("Body JSON obrigatório.")
    try:
        atualizado = atualizar_usuario(usuario_id,
            nome=body.get("nome"), email=body.get("email"),
            telefone=body.get("telefone"), cidade=body.get("cidade"),
            empresa=body.get("empresa"), cpf_cnpj=body.get("cpf_cnpj"))
    except sqlite3.IntegrityError:
        return erro("E-mail ou CPF/CNPJ já pertence a outro cliente.", 409)
    if not atualizado: return erro("Cliente não encontrado.", 404)
    return ok(msg="Cliente atualizado.")

@app.delete("/usuarios/<int:usuario_id>")
def delete_usuario(usuario_id):
    deletado = deletar_usuario(usuario_id)
    if not deletado: return erro("Cliente não encontrado.", 404)
    return ok(msg="Cliente deletado.")

if __name__ == "__main__":
    app.run(debug=True, port=5000)