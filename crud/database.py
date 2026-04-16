import sqlite3
import psycopg2
import os

def get_connection():
    # Se houver DATABASE_URL (nuvem), usa Postgres. Se não, usa SQLite local.
    url = os.environ.get("DATABASE_URL")
    if url:
        return psycopg2.connect(url)
    return sqlite3.connect("banco.db")

def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()
    # Sintaxe compatível com ambos
    sql = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telefone TEXT,
        cidade TEXT,
        empresa TEXT,
        cpf_cnpj TEXT UNIQUE
    );
    """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()