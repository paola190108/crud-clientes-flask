import os
from .database import get_connection

def get_placeholder():
    return "%s" if os.environ.get("DATABASE_URL") else "?"

def criar_usuario(nome, email, telefone=None, cidade=None, empresa=None, cpf_cnpj=None):
    conn = get_connection()
    cursor = conn.cursor()
    p = get_placeholder()
    sql = f"INSERT INTO usuarios (nome, email, telefone, cidade, empresa, cpf_cnpj) VALUES ({p}, {p}, {p}, {p}, {p}, {p})"
    cursor.execute(sql, (nome, email, telefone, cidade, empresa, cpf_cnpj))
    conn.commit()
    cursor.close()
    conn.close()
    return True

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios ORDER BY id DESC")
    usuarios = []
    for row in cursor.fetchall():
        usuarios.append({
            "id": row[0], "nome": row[1], "email": row[2],
            "telefone": row[3], "cidade": row[4], "empresa": row[5], "cpf_cnpj": row[6]
        })
    cursor.close()
    conn.close()
    return usuarios

def buscar_por_nome(nome):
    conn = get_connection()
    cursor = conn.cursor()
    p = get_placeholder()
    op = "ILIKE" if os.environ.get("DATABASE_URL") else "LIKE"
    cursor.execute(f"SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios WHERE nome {op} {p}", (f"%{nome}%",))
    usuarios = []
    for row in cursor.fetchall():
        usuarios.append({
            "id": row[0], "nome": row[1], "email": row[2],
            "telefone": row[3], "cidade": row[4], "empresa": row[5], "cpf_cnpj": row[6]
        })
    cursor.close()
    conn.close()
    return usuarios

def atualizar_usuario(usuario_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    p = get_placeholder()
    campos = [f"{k} = {p}" for k, v in kwargs.items() if v is not None]
    valores = [v for v in kwargs.values() if v is not None]
    valores.append(usuario_id)
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = {p}"
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()
    return True

def deletar_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    p = get_placeholder()
    cursor.execute(f"DELETE FROM usuarios WHERE id = {p}", (usuario_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True