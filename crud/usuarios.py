"""
usuarios.py — Operações CRUD para a tabela de clientes
"""

from .database import get_conn


def criar_usuario(nome, email, telefone=None, cidade=None, empresa=None, cpf_cnpj=None):
    sql = """
        INSERT INTO usuarios (nome, email, telefone, cidade, empresa, cpf_cnpj)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    with get_conn() as conn:
        cursor = conn.execute(sql, (nome, email, telefone, cidade, empresa, cpf_cnpj))
        return cursor.lastrowid


def listar_usuarios():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM usuarios ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def buscar_por_id(usuario_id):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE id = ?", (usuario_id,)
        ).fetchone()
    return dict(row) if row else None


def buscar_por_nome(nome):
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM usuarios WHERE nome LIKE ? ORDER BY nome",
            (f"%{nome}%",)
        ).fetchall()
    return [dict(r) for r in rows]


def buscar_por_email(email):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE email = ?", (email,)
        ).fetchone()
    return dict(row) if row else None


def atualizar_usuario(usuario_id, nome=None, email=None, telefone=None,
                      cidade=None, empresa=None, cpf_cnpj=None):
    campos, valores = [], []
    if nome     is not None: campos.append("nome = ?");     valores.append(nome)
    if email    is not None: campos.append("email = ?");    valores.append(email)
    if telefone is not None: campos.append("telefone = ?"); valores.append(telefone)
    if cidade   is not None: campos.append("cidade = ?");   valores.append(cidade)
    if empresa  is not None: campos.append("empresa = ?");  valores.append(empresa)
    if cpf_cnpj is not None: campos.append("cpf_cnpj = ?"); valores.append(cpf_cnpj)
    if not campos:
        return False
    valores.append(usuario_id)
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = ?"
    with get_conn() as conn:
        cursor = conn.execute(sql, valores)
    return cursor.rowcount > 0


def deletar_usuario(usuario_id):
    with get_conn() as conn:
        cursor = conn.execute(
            "DELETE FROM usuarios WHERE id = ?", (usuario_id,)
        )
    return cursor.rowcount > 0