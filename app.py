import os
from flask import Flask, request, jsonify, render_template

# IMPORTAÇÃO CORRIGIDA:
from crud.database import criar_tabela 
from crud.usuarios import criar_usuario, listar_usuarios, atualizar_usuario, deletar_usuario, buscar_por_nome

app = Flask(__name__)

with app.app_context():
    criar_tabela()

def ok(data=None, status=200, msg=None):
    body = {"status": "ok"}
    if msg: body["mensagem"] = msg
    if data is not None: body["data"] = data
    return jsonify(body), status

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return ok(listar_usuarios())

@app.route("/usuarios", methods=["POST"])
def post_usuario():
    body = request.get_json()
    try:
        criar_usuario(body['nome'], body['email'], body.get('telefone'), 
                      body.get('cidade'), body.get('empresa'), body.get('cpf_cnpj'))
        return ok(status=201, msg="Criado!")
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

@app.route("/usuarios/<int:id>", methods=["PUT"])
def put_usuario(id):
    body = request.get_json()
    atualizar_usuario(id, **body)
    return ok(msg="Atualizado!")

@app.route("/usuarios/<int:id>", methods=["DELETE"])
def delete_user(id):
    deletar_usuario(id)
    return ok(msg="Deletado!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)