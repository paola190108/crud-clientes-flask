from .database import get_connection

def criar_usuario(nome, email, telefone=None, cidade=None, empresa=None, cpf_cnpj=None):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO usuarios (nome, email, telefone, cidade, empresa, cpf_cnpj) 
             VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"""
    cursor.execute(sql, (nome, email, telefone, cidade, empresa, cpf_cnpj))
    novo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return novo_id

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios ORDER BY id DESC")
    colunas = [desc[0] for desc in cursor.description]
    usuarios = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return usuarios

def buscar_por_id(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios WHERE id = %s", (usuario_id,))
    row = cursor.fetchone()
    usuario = None
    if row:
        colunas = [desc[0] for desc in cursor.description]
        usuario = dict(zip(colunas, row))
    cursor.close()
    conn.close()
    return usuario

def buscar_por_nome(nome):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios WHERE nome ILIKE %s", (f'%{nome}%',))
    colunas = [desc[0] for desc in cursor.description]
    usuarios = [dict(zip(colunas, row)) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return usuarios

def buscar_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone, cidade, empresa, cpf_cnpj FROM usuarios WHERE email = %s", (email,))
    row = cursor.fetchone()
    usuario = None
    if row:
        colunas = [desc[0] for desc in cursor.description]
        usuario = dict(zip(colunas, row))
    cursor.close()
    conn.close()
    return usuario

def atualizar_usuario(usuario_id, **kwargs):
    conn = get_connection()
    cursor = conn.cursor()
    # Filtra apenas campos que não são None para atualizar
    campos = [f"{k} = %s" for k, v in kwargs.items() if v is not None]
    valores = [v for v in kwargs.values() if v is not None]
    if not campos: return False
    valores.append(usuario_id)
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"
    cursor.execute(sql, valores)
    linhas = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return linhas > 0

def deletar_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    linhas = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return linhas > 0